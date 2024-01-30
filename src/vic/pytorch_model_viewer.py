

# Visualize a pytorch Model object
# Known properties and variables?
# Can you visualize the structure of the code?
# Start with a resnet 50 or fcn

import dearpygui.dearpygui as dpg
import torch

def add_children_recursively(module):
    for child_name, child in list(module.named_children()):
        if issubclass(type(child), torch.nn.Module):
            # print("TRUE")
            n_children = len(list(child.named_children()))
            if n_children == 0:
                dpg.add_text(child_name + ": " + str(child))
                # from vic import vic
                # vic.interact(locals())
            else:
                with dpg.tree_node(label=child_name):
                    add_children_recursively(child)
        else:
            # print("???")
            dpg.add_text(child)

def interact(model, new_window=True):
    # Pytorch nn.Module
    def vic_callback(sender, app_data, user_data):
        import inspect
        from vic import vic
        vic.interact(locals())

    dpg.create_context()
    window_name = "Model Viewer: {}".format(model.__class__.__name__)
    with dpg.window(label=window_name, tag=window_name):
        dpg.add_button(label="Vic", callback=vic_callback)

        # Modules very messy
        # for module in model.modules():
        #     dpg.add_text(module)
        #     # dpg.add_text(module)
            
        for child_name, child in list(model.named_children()):
            print("Child: ", child_name)
            # from vic import vic
            # vic.interact(locals())
            with dpg.collapsing_header(label=child_name):
                add_children_recursively(child)
                # dpg.add_text(child)
            # dpg.add_text(module)




    # If this is called from an existing dpg window, everything will break
    dpg.create_viewport(title='Pytorch Model Viewer', width=800, height=800)
    # dpg.show_viewport()
    if new_window:
        dpg.setup_dearpygui()
        # dpg.set_primary_window(window_name, True)
        dpg.start_dearpygui()
        dpg.destroy_context()


    pass