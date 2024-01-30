
class VicState:
    def __init__(self,):
        self.reset()
    
    def reset(self):
        self.focused_object = None
        self.focused_object_name = None
        self.focused_object_path = [self.focused_object_name]

        self.selected_attribute = None
        self.selected_attribute_name = None

    def focus_object(self, object_name):
        self.focused_object_path = [object_name]
        
    def set_selected_attribute_name(self, attribute_name):
        self.selected_attribute_name = attribute_name

    def get_selected_attribute_name(self):
        return self.selected_attribute_name

    def focus_selected_attribute(self,):
        if self.selected_attribute_name is not None:
            self.focused_object_path.append(self.selected_attribute_name)
        self.selected_attribute = None
    
    
    def focus_attribute(self, attribute_name):
        self.focused_object_path.append(attribute_name)
    
    def get_selected_attribute(self, locals):
        focused_object = locals[self.focused_object_path[0]]
        path_str = self.focused_object_path[0]
        if len(self.focused_object_path) > 1:
            for attr_name in self.focused_object_path[1:]:
                focused_object = getattr(focused_object, attr_name)
                path_str = f"{path_str}.{attr_name}"
        
        return focused_object, path_str
    

    

