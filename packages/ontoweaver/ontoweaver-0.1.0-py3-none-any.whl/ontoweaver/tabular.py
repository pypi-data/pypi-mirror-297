import sys
import math
import types as pytypes
import logging
from typing import Optional
from collections.abc import Iterable
from enum import Enum, EnumMeta
import ontoweaver

import pandas as pd

from . import base
from . import types
from . import transformer

class MetaEnum(EnumMeta):
    """
    Metaclass for Enum to allow checking if an item is in the Enum.
    """

    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class Enumerable(Enum, metaclass=MetaEnum):
    """
    Base class for Enums with MetaEnum metaclass.
    """
    pass


class TypeAffixes(str, Enumerable):
    """
    Enum for type affixes used in ID creation.
    """
    suffix = "suffix"
    prefix = "prefix"
    none = "none"


class PandasAdapter(base.Adapter):
    """Interface for extracting data from a Pandas DataFrame with a simple mapping configuration based on declared types.

    The general idea is that each row of the table is mapped to a source node,
    and some column values are mapped to an edge leading to another node.
    Some other columns may also be mapped to properties of either a node or an edge.

    The class expect a configuration formed by three objects:
        - the type of the source node mapped for each row.
        - a dictionary mapping each column name to the type of the edge (which contains the type of both the source and target node),
        - a dictionary mapping each (node or edge) type to another dictionary listing which column is extracted to which property.

    Note that, when using the `configure` mapping,
    types are created by default in the `ontoweaver.types` module,
    so that you may access the list of all declared types by using:
        - `ontoweaver.types.all.nodes()`,
        - `ontoweaver.types.all.node_fields()`,
        - `ontoweaver.types.all.edges()`,
        - `ontoweaver.types.all.edge_fields()`.
    """

    def __init__(self,
                 df: pd.DataFrame,
                 subject_transformer: base.Transformer,
                 transformers: Iterable[base.Transformer],
                 type_affix: Optional[TypeAffixes] = TypeAffixes.suffix,
                 type_affix_sep: Optional[str] = ":",
                 ):
        """
        Instantiate the adapter.

        Args:
            df (pd.DataFrame): The table containing the input data.
            subject_transformer (base.Transformer): The transformer that maps the subject node.
            transformers (Iterable[base.Transformer]): List of transformer instances that map the data frame to nodes and edges.
            type_affix (Optional[TypeAffixes]): Where to add a type annotation to the labels (either TypeAffixes.prefix, TypeAffixes.suffix or TypeAffixes.none).
            type_affix_sep (Optional[str]): String used to separate a label from the type annotation (WARNING: double-check that your BioCypher config does not use the same character as a separator).
        """
        super().__init__()

        logging.info("DataFrame info:")
        # logging.info(df.info())
        logging.debug("Columns:")
        for c in df.columns:
            logging.debug(f"\t`{c}`")
        logging.info("\n" + str(df))
        self.df = df

        if not type_affix in TypeAffixes:
            raise ValueError(f"`type_affix`={type_affix} is not one of the allowed values ({[t for t in TypeAffixes]})")
        else:
            self.type_affix = type_affix

        self.type_affix_sep = type_affix_sep

        self.subject_transformer = subject_transformer
        self.transformers = transformers
        # logging.debug(self.properties_of)

    def source_type(self, row):
        """
        Accessor to the row type actually used by `run`.

        You may overload this function if you want
        to make the row type dependent on some column value.

        By default, just return the default row type defined in the constructor,
        without taking the row values into account.

        Args:
            row: The current row of the DataFrame.

        Returns:
            The row type.
        """
        return self.row_type


    def make_id(self, type, entry_name):
        """
        Create a unique id for the given cell consisting of the entry name and type,
        taking into account affix and separator configuration.

        Args:
            type: The type of the entry.
            entry_name: The name of the entry.

        Returns:
            str: The created ID.

        Raises:
            ValueError: If the ID creation fails.
        """
        if self.type_affix == TypeAffixes.prefix:
            id = f'{type}{self.type_affix_sep}{entry_name}'
        elif self.type_affix == TypeAffixes.suffix:
            id = f'{entry_name}{self.type_affix_sep}{type}'
        elif self.type_affix == TypeAffixes.none:
            id = f'{entry_name}'

        if id:
            logging.debug(f"\tID created for cell value `{entry_name}` of type: `{type}`: `{id}`")
            return id
        else:
            raise ValueError(f"Failed to create ID for cell value: `{entry_name}` of type: `{type}`")

    def valid(self, val):
        """
        Checks if cell value is valid - not a `nan`.

        Args:
            val: The value to check.

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        if pd.api.types.is_numeric_dtype(type(val)):
            if (math.isnan(val) or val == float("nan")):
                return False
        elif str(val) == "nan":  # Conversion from Pandas' `object` needs to be explicit.
            return False
        return True

    def properties(self, properity_dict, row, i):
        """
        Extract properties of each property category for the given node type.
        If no properties are found, return an empty dictionary.

        Args:
            properity_dict: Dictionary of property mappings.
            row: The current row of the DataFrame.
            i: The index of the current row.

        Returns:
            dict: Extracted properties.
        """
        properties = {}

        for prop_transformer, property_name in properity_dict.items():
            for property in prop_transformer(row, i):
                properties[property_name] = str(property).replace("'", "`")

        return properties

    def make_node(self, node_t, id, properties):
        """
        Create nodes of a certain type.

        Args:
            node_t: The type of the node.
            id: The ID of the node.
            properties: The properties of the node.

        Returns:
            The created node.
        """
        return node_t(id=id, properties=properties)

    def make_edge(self, edge_t, id_target, id_source, properties):
        """
        Create edges of a certain type.

        Args:
            edge_t: The type of the edge.
            id_target: The ID of the target node.
            id_source: The ID of the source node.
            properties: The properties of the edge.

        Returns:
            The created edge.
        """
        return edge_t(id_source=id_source, id_target=id_target, properties=properties)

    def run(self):
        """Iterate through data frame and map the cell values according to yaml file, using list of transformers."""

        # Loop over the data frame.
        for i, row in self.df.iterrows():

            source_id = None
            source_node_id = None

            # Declare a source id and create corresponding node. If no column defined, create source id from row index.
            if source_id is None:

                for s_id in self.subject_transformer(row, i):
                    source_id =  s_id


                source_node_id = self.make_id(self.subject_transformer.target.__name__, source_id)

            if source_node_id:
                logging.debug(f"\t\tDeclared source id: `{source_node_id}")
                self.nodes_append((self.make_node(node_t=self.subject_transformer.target, id=source_node_id,
                                          properties=self.properties(self.subject_transformer.properties_of, row, i))))
            else:
                raise ValueError(f"\t\tDeclaration of subject ID for row `{row}` unsuccessful.")

            # Loop over list of transformer instances and create corresponding nodes and edges.
            for transformer in self.transformers:

                # TODO assert that there is no from_subject attribute in the regular transforemrs

                    for target_id in transformer(row, i):
                        if target_id:
                            target_node_id = self.make_id(transformer.target.__name__, target_id)
                            logging.debug(f"\t\t\t\tMake node `{target_node_id}`.")
                            self.nodes_append(self.make_node(node_t=transformer.target, id=target_node_id,
                                                      properties=self.properties(transformer.properties_of, row, i)))

                            # If a `from_subject` attribute is present in the transformer, loop over the transformer
                            # list to find the transformer instance mapping to the correct type, and then create new
                            # subject id.

                            # FIXME add hook functions to be overloaded.

                            # FIXME: Make from_subject reference a list of subjects instead of using the add_edge function.

                            if hasattr(transformer, "from_subject"):
                                for t in self.transformers:
                                    if transformer.from_subject == t.target.__name__:
                                        for s_id in t(row, i):
                                            subject_id = s_id
                                        subject_node_id = self.make_id(t.target.__name__, subject_id)
                                        logging.debug(f"\t\t\t\tMake edge from `{subject_node_id}` toward `{target_node_id}`.")
                                        self.edges_append(
                                            self.make_edge(edge_t=transformer.edge, id_source=subject_node_id,
                                                           id_target=target_node_id,
                                                           properties=self.properties(transformer.properties_of, row, i)))

                                    else:
                                        continue
                            else:
                                logging.debug(f"\t\t\t\tMake edge from `{source_node_id}` toward `{target_node_id}`.")
                                self.edges_append(self.make_edge(edge_t=transformer.edge, id_target=target_node_id, id_source=source_node_id,
                                                          properties=self.properties(transformer.edge.fields(), row, i)))
                        else:
                            logging.error(f"\t\tDeclaration of target ID for row `{row}` unsuccessful.")
                            continue

                        # TODO check if two transformers are declaring the same type and raise error

def extract_all(df: pd.DataFrame, config: dict, module=types, affix="suffix", separator=":"):
    """
    Proxy function for extracting from a table all nodes, edges and properties
    that are defined in a PandasAdapter configuration.

    Args:
        df (pd.DataFrame): The DataFrame containing the input data.
        config (dict): The configuration dictionary.
        module: The module in which to insert the types declared by the configuration.
        affix (str): The type affix to use (default is "suffix").
        separator (str): The separator to use between labels and type annotations (default is ":").

    Returns:
        PandasAdapter: The configured adapter.
    """
    parser = ontoweaver.tabular.YamlParser(config, module)
    mapping = parser()

    adapter = PandasAdapter(
        df,
        *mapping,
        type_affix=affix,
        type_affix_sep=separator
    )

    adapter.run()

    return adapter


class Declare:
    """
    Declarations of functions used to declare and instantiate object classes used by the Adapter for the mapping
    of the data frame.

    Args:
        module: The module in which to insert the types declared by the configuration.
    """

    def __init__(self,
                 module=types,
                 ):
        self.module = module

    def make_node_class(self, name, properties={}, base=base.Node):
        """
        Create a node class with the given name and properties.

        Args:
            name: The name of the node class.
            properties (dict): The properties of the node class.
            base: The base class for the node class.

        Returns:
            The created node class.
        """
        # If type already exists, return it.
        if hasattr(self.module, name):
            cls = getattr(self.module, name)
            logging.debug(
                f"\tNode class `{name}` (prop: `{cls.fields()}`) already exists, I will not create another one.")
            for p in properties.values():
                if p not in cls.fields():
                    logging.warning(f"\t\tProperty `{p}` not found in fields.")
            return cls

        def fields():
            return list(properties.values())

        attrs = {
            "__module__": self.module.__name__,
            "fields": staticmethod(fields),
        }
        t = pytypes.new_class(name, (base,), {}, lambda ns: ns.update(attrs))
        logging.debug(f"Declare Node class `{t}` (prop: `{properties}`).")
        setattr(self.module, t.__name__, t)
        return t

    def make_edge_class(self, name, source_t, target_t, properties={}, base=base.Edge, ):
        """
        Create an edge class with the given name, source type, target type, and properties.

        Args:
            name: The name of the edge class.
            source_t: The source type of the edge.
            target_t: The target type of the edge.
            properties (dict): The properties of the edge class.
            base: The base class for the edge class.

        Returns:
            The created edge class.
        """
        # If type already exists, return it.
        if hasattr(self.module, name):
            cls = getattr(self.module, name)
            logging.info(
                f"Edge class `{name}` (prop: `{cls.fields()}`) already exists, I will not create another one.")
            for t, p in properties.items():
                if p not in cls.fields():
                    logging.warning(f"\t\tProperty `{p}` not found in fields.")

            tt_list = cls.target_type()

            tt_list.append(target_t)

            def tt():
                return tt_list

            cls.target_type = staticmethod(tt)

            # TODO allow multiple source types for edge

            return cls

        def fields():
            return properties

        def st():
            return source_t

        def tt():
            return [target_t]

        attrs = {
            "__module__": self.module.__name__,
            "fields": staticmethod(fields),
            "source_type": staticmethod(st),
            "target_type": staticmethod(tt),
        }
        t = pytypes.new_class(name, (base,), {}, lambda ns: ns.update(attrs))
        logging.debug(f"Declare Edge class `{t}` (prop: `{properties}`).")
        setattr(self.module, t.__name__, t)
        return t

    def make_transformer_class(self, transformer_type, node_type=None, properties=None, edge=None, columns=None, **kwargs):
        """
        Create a transformer class with the given parameters.

        Args:
            transformer_type: The type of the transformer.
            node_type: The type of the node.
            properties: The properties of the transformer.
            edge: The edge type of the transformer.
            columns: The columns to be processed by the transformer.
            **kwargs: Additional keyword arguments.

        Returns:
            The created transformer class.

        Raises:
            TypeError: If the transformer type is not an existing transformer.
        """
        if hasattr(transformer, transformer_type):
            parent_t = getattr(transformer, transformer_type)
            kwargs.setdefault("subclass", parent_t)
            if not issubclass(parent_t, base.Transformer):
                raise TypeError(f"Object `{transformer_type}` is not an existing transformer.")
            else:
                logging.debug(f"Declare transformer type '{transformer_type}' for node type '{node_type}'")
                return parent_t(target=node_type, properties_of=properties, edge=edge, columns=columns,
                                        **kwargs)
        else:
            # logging.debug(dir(generators))
            raise TypeError(f"Cannot find a transformer of name `{transformer_type}`.")


class YamlParser(Declare):
    """
    Parse a table extraction configuration and return the three objects needed to configure an Adapter.

    The config is a dictionary containing only strings, as converted from the following YAML description:

    .. code-block:: yaml

            row:
               map:
                  columns:
                    - <MY_COLUMN_NAME>
                  to_subject: <MY_SUBJECT_TYPE>
            transformers:
                - map:
                    columns:
                        - <MY_COLUMN_NAME>
                    to_object: <MY_OBJECT_TYPE>
                    via_relation: <MY_RELATION_TYPE>
                - map:
                    columns:
                        - <MY_OTHER_COLUMN>
                    to_property:
                        - <MY_PROPERTY>
                    for_objects:
                        - <MY_OBJECT_TYPE>

    This maps the table row to a MY_SUBJECT_TYPE node type, adding an edge of type MY_RELATION_TYPE,
    between the MY_SUBJECT_TYPE node and another MY_OBJECT_TYPE node. The data in MY_OTHER_COLUMN is mapped
    to the MY_PROPERTY property of the MY_OBJECT_TYPE node. Note that `to_properties` may effectively map to
    an edge type or several types.

    In order to allow the user to write mappings configurations using their preferred vocabulary, the following
    keywords are interchangeable:
        - subject = row = entry = line,
        - columns = fields,
        - to_target = to_object = to_node
        - via_edge = via_relation = via_predicate.

    :param dict config: A configuration dictionary.
    :param module: The module in which to insert the types declared by the configuration.
    :return tuple: subject_transformer, transformers, as needed by the Adapter.
    """

    def __init__(self, config: dict, module=types):
        """
        Initialize the YamlParser.

        Args:
            config (dict): The configuration dictionary.
            module: The module in which to insert the types declared by the configuration.
        """
        super().__init__(module)
        self.config = config

        logging.debug(f"Classes created in module '{self.module}'")

    def get_not(self, keys, pconfig=None):
        """
        Get the first dictionary (key, item) not matching any of the passed keys.

        Args:
            keys: The keys to exclude.
            pconfig: The configuration dictionary to search in (default is self.config).

        Returns:
            dict: The first dictionary not matching any of the passed keys.
        """
        res = {}
        if not pconfig:
            pconfig = self.config
        for k in pconfig:
            if k not in keys:
                res[k] = pconfig[k]
        return res

    def get(self, keys, pconfig=None):
        """
        Get a dictionary item matching any of the passed keys.

        Args:
            keys: The keys to search for.
            pconfig: The configuration dictionary to search in (default is self.config).

        Returns:
            The first item matching any of the passed keys, or None if no match is found.
        """
        if not pconfig:
            pconfig = self.config
        for k in keys:
            if k in pconfig:
                return pconfig[k]
        return None

    def __call__(self):
        """
        Parse the configuration and return the subject transformer and transformers.

        Returns:
            tuple: The subject transformer and a list of transformers.
        """
        properties_of = {}
        transformers = []

        # Various keys are allowed in the config to allow the user to use their favorite ontology vocabulary.
        k_row = ["row", "entry", "line", "subject", "source"]
        k_subject_type = ["to_subject"]
        k_columns = ["columns", "fields"]
        k_target = ["to_target", "to_object", "to_node"]
        k_subject = ["from_subject", "from_source"]
        k_edge = ["via_edge", "via_relation", "via_predicate"]
        k_properties = ["to_properties", "to_property"]
        k_prop_to_object = ["for_objects"]
        k_transformer = ["transformers"]

        transformers_list = self.get(k_transformer)

        # First, parse property mappings.
        for transformer_types in transformers_list:
            for transformer_type, field_dict in transformer_types.items():
                if any(field in field_dict.keys() for field in k_properties):
                    object_types = self.get(k_prop_to_object, pconfig=field_dict)
                    property_names = self.get(k_properties, pconfig=field_dict)
                    column_names = self.get(k_columns, pconfig=field_dict)
                    prop_transformer = self.make_transformer_class(transformer_type, columns=column_names)
                    for object_type in object_types:
                        properties_of.setdefault(object_type, {})
                        for property_name in property_names:
                            properties_of[object_type].setdefault(prop_transformer, property_name)
                        logging.debug(f"\t\t\t\tDeclare property mapping for `{object_type}`: {properties_of[object_type]}")

        subject_dict = self.get(k_row)
        subject_transformer_class = list(subject_dict.keys())[0]
        subject_type = self.get(k_subject_type, subject_dict[subject_transformer_class])
        subject_kwargs = self.get_not(k_subject_type + k_columns, subject_dict[subject_transformer_class])
        subject_columns = self.get(k_columns, subject_dict[subject_transformer_class])
        logging.debug(f"Declare subject of type: '{subject_type}', subject transformer: '{subject_transformer_class}', "
                      f"subject kwargs '{subject_kwargs}', subject columns '{subject_columns}'")

        source_t = self.make_node_class(subject_type, properties_of.get(subject_type, {}))
        subject_transformer = self.make_transformer_class(
            columns=subject_columns, transformer_type=subject_transformer_class,
            node_type=source_t, properties=properties_of.get(subject_type, {}), **subject_kwargs)

        # Then, declare types.
        for transformer_types in transformers_list:
            for transformer_type, field_dict in transformer_types.items():
                if any(field in field_dict.keys() for field in k_properties):
                    if any(field in field_dict.keys() for field in k_target):
                        prop = self.get(k_properties, field_dict)
                        target = self.get(k_target, field_dict)
                        logging.error(f"ERROR in transformer '{transformer_type}': one cannot "
                                      f"declare a mapping to both properties '{prop}' and object type '{target}'.")
                    continue
                else:
                    columns = self.get(k_columns, pconfig=field_dict)
                    target = self.get(k_target, pconfig=field_dict)
                    subject = self.get(k_subject, pconfig=field_dict)
                    edge = self.get(k_edge, pconfig=field_dict)
                    gen_data = self.get_not(k_target + k_edge + k_columns, pconfig=field_dict)

                    # Harmonize the use of the `from_subject` and `from_source` synonyms in the configuration, because
                    # from_subject` is used in the transformer class to refer to the source node type.
                    if 'from_source' in gen_data:
                        gen_data['from_subject'] = gen_data['from_source']
                        del gen_data['from_source']

                    if target and edge:
                        target_t = self.make_node_class(target, properties_of.get(target, {}))
                        logging.debug(f"\t\t\t\tDeclare target for `{target}`: {target_t}")
                        if subject:
                            subject_t = self.make_node_class(subject, properties_of.get(subject, {}))
                            edge_t = self.make_edge_class(edge, subject_t, target_t, properties_of.get(edge, {}))
                        else:
                            edge_t = self.make_edge_class(edge, source_t, target_t, properties_of.get(edge, {}))
                        transformers.append(self.make_transformer_class(
                            transformer_type=transformer_type, node_type=target_t,
                            properties=properties_of.get(target, {}), edge=edge_t, columns=columns, **gen_data))
                        logging.debug(f"\t\t\t\tDeclare mapping `{columns}` => `{edge_t.__name__}`")
                    elif (target and not edge) or (edge and not target):
                        logging.error(f"\t\t\t\tCannot declare the mapping  `{columns}` => `{edge}` (target: `{target}`)")

        logging.debug(f"source class: {source_t}")
        logging.debug(f"properties_of: {properties_of}")
        logging.debug(f"transformers: {transformers}")
        return subject_transformer, transformers