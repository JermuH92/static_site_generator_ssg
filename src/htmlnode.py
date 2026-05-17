class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        output = ''

        if self.props is None:
            return ''
        
        for k, v in self.props.items():
            output += f' {k}="{v}"'
        
        return output

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value.")

        if self.tag is None:
            return self.value
    
        props_string = self.props_to_html()

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: ParentNode must have a tag.")
        
        if self.children is None:
            raise ValueError("Error: ParentNode children are missing a value.")
        
        html_string = ""

        for child in self.children:
            html_string += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"