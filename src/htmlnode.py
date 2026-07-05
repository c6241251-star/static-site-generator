class HTMLNode:
    def __init__(
            self, 
            tag:   str | None                 = None, 
            value: str | None                 = None, 
            children: list["HTMLNode"] | None = None, 
            props:    dict[str, str]   | None = None
        ) -> None:
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self) -> str:
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""
        return "".join([f' {key}="{self.props[key]}"' for key in self.props])
    
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag:str, 
            value:str, 
            props: dict[str, str] | None = None
        ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None or self.value.strip() == "":
            raise ValueError("must have a value")
        if self.tag is None or self.tag.strip() == "":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})"
