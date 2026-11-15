
class HTMLNode:
    def __init__(self, tag: str | None=None, value: str | None=None, children: list | None=None, props: dict | None=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == "" or self.props is None:
            return ""
        else:
            string = ""
            for key in self.props:
                string += f' {key}="{self.props[key]}"'
            return string

    def __repr__(self) -> str:
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.props = props


    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f"{self.tag}, {self.value}, {self.props}"
class ParentNode(HTMLNode):
    def __init__(self, tag: str , children: list , props: dict | None = None) -> None:
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError ("tag missing")
        if self.children is None:
            raise ValueError ("children missing")
        else:
            return(f'<{self.tag}>{self.props_to_html()}{self.parent_to_html_helper("")}</{self.tag}>')

    def parent_to_html_helper(self, result):
        if self.children is not None:
            for child in self.children:
                result += child.to_html()
            return result
