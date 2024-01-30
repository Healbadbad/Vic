# from dearpygui.dearpygui import *
from distutils.log import error
import dearpygui.dearpygui as dpg
import inspect
import traceback
import pprint

try:
    from vicstate import VicState
    import inspect_tools
except:
    from vic.vicstate import VicState
    import vic.inspect_tools as inspect_tools 



def interact(locals, do_traceback=False, ignore_builtins=True, show_tensors=False):
    """ Open a PySimpleGUI window displaying
        local modules, objects, and callables.

        set ignore_builtins=True to hide all attributes with "__" at the beginning of their name
    """
    print("ignore_builtins is ", ignore_builtins)
    print("show_tensors is ", show_tensors)
    now_locals_names = list(locals)
    stack = inspect.stack(4)
    trace = inspect.trace(4)
    # print("stack: ", stack)
    # print("trace: ", trace)
    #print("traceback: ", traceback.print_exc())

    #traceback.print_exc()
    traceback_string = traceback.format_exc()
    # trace_frames = traceback.extract_stack()
    # for frame in trace_frames:
    #     print(frame)
    #     print(frame.line)
    # extracted_tb = traceback.extract_tb()

    if do_traceback:
        print("")
        print("---- Traceback ---- ")
        print(traceback_string)
        # print(extracted_tb)

    # print("Current stack")
    # for frame in stack:
    #     context = frame.code_context
    #     for line in context:
    #         print(line)

    state = VicState()

    dpg.create_context()

    def button_callback(sender, app_data, user_data):
        print(f"sender is: {sender}")
        print(f"app_data is: {app_data}")
        print(f"user_data is: {user_data}")
    
    def font_scale_callback(sender, app_data, user_data):
        dpg.set_global_font_scale(dpg.get_value(sender))
    
    def attributes_listbox_select_callback(sender, app_data, user_data):
        # attributes are stored as strings in the listbox
        # get the attribute name from the string
        attr_name = app_data.split(':')[0]
        print(attr_name, " selected") 
        print(state.focused_object_path)
        print(state.selected_attribute_name)
        state.set_selected_attribute_name(attr_name)

        selected_object, attribute_path = state.get_selected_attribute(locals)
        docstr = getattr(selected_object, attr_name).__doc__
        if docstr is None or docstr == "":
            docstr = f"No Docstring avalable for {attribute_path}"
        try:
            #sig = inspect.signature(getattr(locals[focused_object_name], selected_function_name))
            print("full arg spec:", inspect.getfullargspec(getattr(selected_object, attr_name)))
            sig = inspect.signature(getattr(selected_object, attr_name))
        except Exception as e:
            print("Error getting signature:", e)

            sig = " -- Unable to retrieve signature "

        displaystr = f"{attribute_path}.{attr_name}" + str(sig) + "\n\n" + str(docstr)
        dpg.set_value("docstring_textbox", displaystr)

    
    def object_focus_callback(sender, app_data, user_data):
        # print("--- object focus ---")
        # print(f"app_data is: {app_data}")
        # print(f"user_data is: {user_data}")
        # print("focusing object: ", sender)
        # print("sender value: ", dpg.get_value(sender))
        
        state.reset()
        #state.focus_object(sender)
        state.focus_object(user_data)
        selected_object, attribute_path = state.get_selected_attribute(locals)
        focus_object(selected_object, attribute_path)
    
    def focus_attribute_callback(sender, app_data, user_data):
        # All required info is in the state object
        state.focus_selected_attribute()
        selected_object, attribute_path = state.get_selected_attribute(locals)
        focus_object(selected_object, attribute_path)
        docstr = getattr(selected_object, attribute_path).__doc__
        if docstr is None or docstr == "":
            docstr = f"No Docstring avalable for {attribute_path}"
        dpg.set_value("docstring_textbox", docstr)
    
    def focus_object(object, object_path):
        attributes_list, functions = inspect_tools.get_attributes_list(object, ignore_builtins)
        pp = pprint.PrettyPrinter()
        representation = pp.pformat(object)

        dpg.configure_item("attributes-listbox", items=attributes_list)
        dpg.configure_item("functions-listbox", items=functions)
        dpg.set_value("focused-object-path", object_path)
        dpg.set_value("value_textbox", representation)
        dpg.set_value("docstring_textbox", "")

    def list_to_buttons(items, callback):
        for item in items:
            dpg.add_button(label=item, user_data=item, callback=callback)
    
    def call_attempt(sender, app_data, user_data):
        # Try to call the selected function and print out the result
        # Only possible if no args are required
        #state.focus_selected_attribute()
        selected_object, attribute_path = state.get_selected_attribute(locals)
        #focus_object(selected_object, attribute_path)
        callable_name = state.get_selected_attribute_name()
        callable = getattr(selected_object, callable_name)
        print(f"Trying to call {attribute_path}.{callable_name}")
        try:
            #print("full arg spec:", inspect.getfullargspec(getattr(selected_object, callable_name)))
            sig = inspect.signature(getattr(selected_object, callable_name))
            if no_required_args(sig):
                print(f"Trying to call {attribute_path}.{callable_name} with signature")
                result = callable()
                dpg.set_value("value_textbox", str(result))
            else:
                error_msg = f"Callable {attribute_path}.{callable_name} requires arguments, wich are not yet supported by this tool"
                dpg.set_value("value_textbox", error_msg)
        except (TypeError, ValueError) as e:
            try:
                print(f"Trying to call {attribute_path}.{callable_name} without signature")
                result = callable()
                dpg.set_value("value_textbox", str(result))
            except Exception as e:
                # error_msg = f"Callable {attribute_path}.{callable_name} requires arguments, wich are not yet supported by this tool"
                error_msg = f"Callable {attribute_path}.{callable_name} raised an exception: {e}"
                dpg.set_value("value_textbox", error_msg)

        # dpg.set_value("value_textbox", representation)

        # docstr = getattr(selected_object, attribute_path).__doc__
        # if docstr is None or docstr == "":
        #     docstr = f"No Docstring avalable for {attribute_path}"
        # dpg.set_value("docstring_textbox", docstr)




    def key_press_callback(sender, data):
        # dpg.add_data("run_condition", False)
        dpg.run_condition = False
        #dpg.cleanup_dearpygui()
        # dpg.destroy_context()

    modules = inspect_tools.get_modules(locals)
    callables = inspect_tools.get_functions(locals)
    tensors = inspect_tools.get_tensors(locals)
    local_vars = inspect_tools.list_uniques(list(locals), modules)
    local_vars = inspect_tools.list_uniques(local_vars, callables)
    # local_vars = inspect_tools.list_uniques(local_vars, tensors)
    local_vars = inspect_tools.filter_builtins(local_vars, ignore_builtins)

    with dpg.window(tag="Primary Window"):
        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Escape, callback=key_press_callback)
        dpg.add_text("Hello, world")
        dpg.add_button(label="Save", callback=button_callback)
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=1.0, max_value=3.0, callback=font_scale_callback)
        dpg.add_button(label="Save", callback=button_callback)
        dpg.add_text("Focused object: ", tag="focused-object-path")
        with dpg.child_window(label="test", tag="inspector window", autosize_x=True, height=500):
            with dpg.group(horizontal=True, width=0):
                with dpg.child_window(width=300):
                    with dpg.tab_bar():
                        with dpg.tab(label="local vars"):
                            list_to_buttons(local_vars, object_focus_callback)
                        with dpg.tab(label="modules"):
                            list_to_buttons(modules, object_focus_callback)
                        with dpg.tab(label="callables"):
                            list_to_buttons(callables, object_focus_callback)
                        with dpg.tab(label="tensors"):
                            list_to_buttons(tensors, object_focus_callback)


                with dpg.child_window(width=600):
                    # modules, local_vars, functions = add_locals_buttons(ignore_builtins=ignore_builtins)
                    # dpg.add_column(modules)
                    # dpg.add_column(local_vars)
                    # dpg.add_column(functions)
                    # dpg.add_button(label="test")
                    num_items = 27
                    #att_list = dpg.add_listbox([], label="attributes", tag="attributes-listbox", num_items=num_items, callback=attributes_listbox_select_callback)
                    att_list = dpg.add_listbox([], tag="attributes-listbox", num_items=num_items, callback=attributes_listbox_select_callback)
                    with dpg.popup(dpg.last_item()):
                        dpg.add_text("Attribute options")
                        dpg.add_separator()
                        dpg.add_selectable(label="inspect", user_data=["inspect"], callback=focus_attribute_callback)

                with dpg.child_window(width=600):
                    func_list = dpg.add_listbox([], label="functions", tag="functions-listbox", num_items=num_items, callback=attributes_listbox_select_callback)
                    with dpg.popup(dpg.last_item()):
                        dpg.add_text("callable options")
                        dpg.add_separator()
                        dpg.add_selectable(label="inspect", user_data=["inspect"], callback=focus_attribute_callback)
                        dpg.add_selectable(label="attempt to call", user_data=["inspect"], callback=call_attempt)
                    # dpg.add_listbox([], label="attributes", tag="attributes-listbox", callback=object_focus_callback)
        #with dpg.child_window(autosize_x=True):
        with dpg.group():
            with dpg.group(horizontal=True, width=0):
                dpg.add_input_text(tag="value_textbox", multiline=True, default_value="Value", height=300, width=600, tab_input=True, )
                dpg.add_input_text(tag="docstring_textbox", multiline=True, default_value="docstring", height=300, width=600, tab_input=True, )

    # dpg.show_style_editor()

    dpg.create_viewport(title='Custom Title', width=1300, height=1000)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)

    # dpg.add_data("run_condition", True)
    dpg.run_condition = True
    while dpg.is_dearpygui_running():
        #if not dpg.get_data("run_condition"): break
        if not dpg.run_condition: break
        dpg.render_dearpygui_frame()
    dpg.cleanup_dearpygui()

    #dpg.start_dearpygui()
    #dpg.destroy_context()


    # Font scaling 
    # with dpg.font_registry():
        
    #     # add font (set as default for entire app)
    #     dpg.add_font("/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Regular.otf", CURRENT_DPI * 13, default_font=True)

def no_required_args(signature):
    params = signature.parameters
    for param in params:
        if params[param].default is inspect.Parameter.empty:
            return False
    return True

if __name__ == '__main__':
    stack = inspect.stack(1)
    frame = stack[0]
    sig = inspect.signature(getattr(frame, 'count'))
    sig2 = inspect.signature(getattr(stack, 'reverse'))
    no_req = no_required_args(sig)
    no_req2 = no_required_args(sig2)

    interact(locals=locals())