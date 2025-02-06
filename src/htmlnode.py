class HTMLNode():
    def __init__(self, tag:str=None, value:str=None, children:list["HTMLNode"]=None, props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf Node does not have value")
        if not self.tag:
            return self.value
        space = " " if self.props else ""
        return f"<{self.tag}{space}{self.props_to_html()}>{self.value}</{self.tag}>"
        