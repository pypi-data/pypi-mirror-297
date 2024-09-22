# Written by: Chaitanya S Lakkundi (chaitanya.lakkundi@gmail.com)

import requests
import copy
import json
from .utils import Node, ikml_to_anytree, dict_to_anytree, PreOrderIter

class IKML_Document:
    INDENT = 2
    def __init__(self, url=None, data=None):
        # does dummy root exist or not
        self.exclude_root = False
        # auto load
        self.load(url=url, data=data)

    def mount(self, root):
        # mount root node
        self.root = root

    def load(self, url=None, data=None):
        if url is not None:
            self.url = url
            self.raw_data = str(requests.get(self.url).content, encoding="utf-8")
            self.root = ikml_to_anytree(self.raw_data)
            self.exclude_root = True
        
        if data is not None:
            # data is either a dict or a list of dicts
            if isinstance(data, dict) or isinstance(data, list):
                self.raw_data = data
                self.root = dict_to_anytree(self.raw_data)
            else:
                self.raw_data = data
                self.root = ikml_to_anytree(self.raw_data)
            self.exclude_root = True

    def save(self, filename="out_ikml.txt"):
        with open(filename, "w", encoding="utf-8") as fd:
            fd.write(self.to_txt())

    def to_dict(self, recurse_on_children=True):
        # dot-attributes are automatically added for its parent node
        return self.root.to_dict(recurse_on_children=recurse_on_children)

    def to_json(self, recurse_on_children=True):
        d = self.to_dict(recurse_on_children=recurse_on_children)
        return json.dumps(d, ensure_ascii=False, indent=self.INDENT)

    # TODO: implement exclude_root in to_xml and tree_as_xml_list
    def to_xml(self):
        r2 = copy.deepcopy(self.root)
        # put_attrs_inside is only required for to_xml method.
        # to_dict and to_json check for attributes appropriately by default
        r2.put_attrs_inside()
        return r2.to_xml(quoted_attr=True)
    
    def to_txt(self):
        # returns IKML text
        out = "\n".join(Node.tree_as_list(self.root, exclude_root=self.exclude_root, quoted_attr=False))
        return out

    def tags(self, format="node"):
        out = []
        for n in self.root.node_children:
            # out.append(str(n))
            match format:
                case "node":
                    out.append(n)
                case "dict":
                    out.append(n.to_dict(recurse_on_children=False))
        return out

    def child_tags(self, tag_id, format="node"):
        for node in self.iter():
            try:
                if node["id"] == tag_id:
                    # return [str(n) for n in node.node_children]
                    match format:
                        case "node":
                            return [n for n in node.node_children]
                        case "dict":
                            return [n.to_dict(recurse_on_children=False) for n in node.node_children]
            except:
                pass
        return f"Node with id {tag_id} not found."
    
    # TODO: implement expand_inline
    def find_children(self, tag_name, expand_inline=False, format="node"):
        for node in self.iter():
            try:
                if node.tag_name == tag_name:
                    match format:
                        case "node":
                            yield node
                        case "dict":
                            yield node.to_dict()
            except:
                pass
        return f"Nodes with tag_name {tag_name} not found."

    def get(self, tag_id, format="node"):
        for node in PreOrderIter(self.root):
            try:
                if node["id"] == tag_id:
                    match format:
                        case "dict":
                            return node.to_dict()
                        case "xml":
                            return node.to_xml()
                        case "txt":
                            return node.to_txt()
                        case "node":
                            return node
            except:
                pass
        return f"Node with id {tag_id} not found."
    
    def iter(self):
        for node in PreOrderIter(self.root):
            yield node
    
    @staticmethod
    def create_node(data, *args, **kwargs):
        data = data.strip()
        if data[0] != "[":
            data = f"[{data}]"
        return Node(data, *args, **kwargs)
