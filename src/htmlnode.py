class HTMLNode:
    def __init__(self, *, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""

        return ''.join(f' {key}="{value}"' for key, value in self.props.items()) #value should be html.escape(value, quote=True)
    
    def children_to_string(self):
        if self.children is None:
            return ""
        
        return ', '.join(child.__repr__() for child in self.children)
    

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, attributes:{self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self, *, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError
        elif self.tag is None:
            return self.value
        else:
            if self.props is None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"