class HTMLNode:
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Should be overwritten by subclasses!")

    def props_to_html(self):
        if self.props is None:
            return ""
        output = ""
        for property, value in self.props.items():
            output += f' {property}="{value}"'
        return output

    def __repr__(self):
        return f"HTMLNode, tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        if self.value is None:
            raise ValueError("All LeafNodes must have a value!")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, props=props, children=children)

    def to_html(self): 
        if self.tag is None:
            raise ValueError("All ParentNodes must have a tag!")
        if self.children is None:
            raise ValueError("All ParentNodes must have atleast one child")

        output = map(lambda child: f'{child.to_html()}', self.children)
        return f'<{self.tag}{self.props_to_html()}>{"".join(output)}</{self.tag}>'

