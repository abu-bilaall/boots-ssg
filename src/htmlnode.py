import html

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

        return ''.join(f' {key}="{html.escape(str(value), quote=True)}"' for key, value in self.props.items())
    
    def children_to_string(self):
        if self.children is None:
            return ""
        
        return ', '.join(child.__repr__() for child in self.children)
    

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, attributes:{self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self, *, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.value = html.escape(str(self.value), quote=True)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value
        else:
            if self.props is None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, *, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag must be defined.")
        elif not self.children:
            raise ValueError("Children are missing.")
        else:
            children_tags = "".join(child.to_html() for child in self.children)
            
            if self.props is None:
                return f"<{self.tag}>{children_tags}</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{children_tags}</{self.tag}>"