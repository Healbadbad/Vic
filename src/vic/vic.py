
# operates like import code; code.interact(local=locals())

# Creates a pysimplegui window

# lists all of the local variables

# allows selection of a local variable
# Shows all of its properties and functions

# Has a list of properties and displays their values
# Creates a sidebar with buttons
#   These buttons can be clicked to call the respective function
#   If they have arguments, display their names, and create input fields
#     ### Can create/train a model to predict which local variables can be placed in those fields
#   # These button clicks can be recorded in a selectable text box, output as raw python code that can be copied  
#   # exit button allows the program to continue running, and the window wont pop up again until an error is caught

# TODO: Right click on an attribute to add it to the list of locals that can be explored 

import PySimpleGUI as sg
import inspect
import traceback

sg.theme('DarkAmber')   # Add a touch of color


def interact(locals, do_traceback=False, ignore_builtins=False, show_tensors=False):
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

    def get_locals_buttons(ignore_builtins=True):
        local_vars = []
        functions = []
        modules = []
        for local_var in now_locals_names:
            if local_var.startswith('__') and ignore_builtins:
                continue
            if inspect.ismodule(locals[local_var]):
                modules.append([sg.Button(local_var)])
                continue
            if callable(locals[local_var]):
                functions.append([sg.Button(local_var)])
                continue

            # Torch and numpy inspection tools 
            if hasattr(locals[local_var], 'T'):
                # Assumed to be a torch tensor
                # tensor_shape = str(locals[local_var].shape)
                local_vars.append([sg.Button(f"{local_var} : {locals[local_var].shape}", key=local_var)]) # onclick = property_click_fun
                continue

            local_vars.append([sg.Button(local_var, key=local_var)])
        return modules, local_vars, functions


    def get_attributes_list(var):
        variable_properties = []
        callables = []
        prop_values = []
        for i, prop in enumerate(dir(var)):
            if prop.startswith('__') and ignore_builtins:
                continue

            try:
                is_callable = callable(getattr(var, prop))
            except Exception as e:
                callables.append(f"{prop}: {Exception}")
                continue

            if is_callable:
                callables.append(f"{prop}: {type(getattr(var, prop))}")
            else:
                try:
                    variable_properties.append(f"{prop}: {getattr(var, prop)}")
                except Exception as e:
                    variable_properties.append(f"{prop}: {Exception}")

        return variable_properties, callables

    functions_list_key = "functions_list"
    def generate_layout(focused_object_name, ignore_builtins=False, show_tensors=False):
        interact_textbox = sg.Input(key='interact-textbox')
        execute_button = sg.Button('Execute', key='execute-button')
        builtins_checkbox = sg.Checkbox("Show Builtins", not ignore_builtins, key="show-builtins", enable_events=True)
        show_tensors_checkbox = sg.Checkbox("Show Tensors", show_tensors, key="show-tensors", enable_events=True)

        modules, local_vars, functions = get_locals_buttons(ignore_builtins)
        props, funs = get_attributes_list(focused_object_name)
        locals_layout = [[sg.Column(modules, key="modules-column"), sg.Column(local_vars, key="local-vars-column"), sg.Column(functions, key='functions-column'),]]
        locals_column = sg.Frame("Local objects", [[sg.Column(locals_layout, scrollable=True, expand_x=True, expand_y=True)]], size=(80,30), expand_x=True, expand_y=True )


        attributes_right_click_menu = ['Attr', ['inspect-attribute']]
        attributes_listbox = sg.Listbox(props, size=(80, 30), key='attributes', right_click_menu=attributes_right_click_menu)

        functions_listbox_size = (50, 30)
        functions_listbox = sg.Listbox(funs, size=functions_listbox_size, key=functions_list_key, enable_events=True)

        docstring_textbox_size = (80, detailed_info_height)
        docstring_textbox = sg.Multiline("docstring will be displayed here", size=docstring_textbox_size, key='docstring')

        var_val_str = focused_object_name
        var_value = sg.Multiline(var_val_str, size=(90, detailed_info_height), key='var_value')
        #TODO set variable info here
        variable_frame = sg.Frame('Variable Info', [[var_value]], key='var_name')
        docstring_box = sg.Frame('Docstring',[[docstring_textbox]])



        layout = [ [sg.Button("EXIT"), sg.Text('Locals'), builtins_checkbox, show_tensors_checkbox, interact_textbox, execute_button],
            [sg.Text('Modules'), sg.Text('Objects'), sg.Text('Callables')],
            [locals_column, attributes_listbox, functions_listbox],
            [variable_frame, docstring_box],
                ]

        return layout

    #  minlen, max()
    detailed_info_height = 20
    focused_object_name = now_locals_names[-1]
    focused_object_path = [focused_object_name]

    layout = generate_layout(focused_object_name, ignore_builtins, show_tensors)

    # Create the Window
    font_size = 10
    font_str = 'Helvetica ' + str(font_size)
    sg.set_options(font=font_str)
    window = sg.Window('Visual Inspection of Code (python)', layout, return_keyboard_events=False)
    window.finalize()

    if do_traceback:
        window['docstring'].update(traceback_string)
    window.bind("<Escape>", "-ESCAPE-")

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        # print("event", event)
        # print("values", values)
        if event == sg.WIN_CLOSED or event == 'Cancel' or event == '-ESCAPE-': # if user closes window or clicks cancel
            break
        if event == "EXIT":
            exit(1)
        # inspect a function that was clicked on
        if event == functions_list_key: 
            selected_function_name = values[functions_list_key][0].split(':')[0]
            # attribute_name = values['attributes'][0].split(':')[0]
            focused_object = locals[focused_object_path[0]]
            path_str = focused_object_path[0]
            if len(focused_object_path) > 1:
                for attr_name in focused_object_path[1:]:
                    focused_object = getattr(focused_object, attr_name)
                    path_str = f"{path_str}.{attr_name}"

            #docstr = getattr(locals[focused_object_name], selected_function_name).__doc__
            docstr = getattr(focused_object, selected_function_name).__doc__
            if docstr is None or docstr == "":
                docstr = f"No Docstring avalable for {selected_function_name}"


            # Retrieve function signature
            try:
                #sig = inspect.signature(getattr(locals[focused_object_name], selected_function_name))
                sig = inspect.signature(getattr(focused_object, selected_function_name))
            except:
                sig = " -- Unable to retrieve signature "

            displaystr = f"{path_str}.{selected_function_name}" + str(sig) + "\n\n" + str(docstr)

            window['docstring'].update(displaystr)

            continue

        elif event == "show-builtins":
            ignore_builtins = not ignore_builtins
            print("ignore builtins is now: ", ignore_builtins)
            old_docstring = window['docstring'].DefaultText
            new_layout = generate_layout(focused_object_name, ignore_builtins)
            new_window = sg.Window('Window Title', new_layout, return_keyboard_events=False)
            window.Close()
            window = new_window
            window.finalize()
            window['docstring'].update(old_docstring)
            window.bind("<Escape>", "-ESCAPE-")
            continue

        elif event == "show-tensors":
            show_tensors = not show_tensors
            continue

        elif event == "execute-button":
            print("code to execute:", values['interact-textbox'])
            print("Executing")
            try:
                exec(values['interact-textbox'])
            except Exception as e:
                print("Exception {Exception}")
                print(e)
            continue
        if event == "inspect-attribute":
            # focused_object_name = event
            if len(values['attributes']) < 1:
                print("No attribute selected")
                continue
            attribute_name = values['attributes'][0].split(':')[0]
            focused_object_path.append(attribute_name)
            focused_object = locals[focused_object_path[0]]
            path_str = focused_object_path[0]
            if len(focused_object_path) > 1:
                for attr_name in focused_object_path[1:]:
                    focused_object = getattr(focused_object, attr_name)
                    path_str = f"{path_str}.{attr_name}"

            # Only update These if the buttons were selected
            attributes_list, functions = get_attributes_list(focused_object)
            window['attributes'].update(attributes_list)
            window['functions_list'].update(functions)

            #window['var_name'].update(f"{focused_object_name}.{attribute}")
            window['var_name'].update(path_str)

            var_val_str = str(focused_object)
            window['var_value'].update(var_val_str)
            continue
            
        else:
            focused_object_name = event
            focused_object_path = [focused_object_name]
            # Only update These if the buttons were selected
            attributes_list, functions = get_attributes_list(locals[focused_object_name])
            window['attributes'].update(attributes_list)
            window['functions_list'].update(functions)
            window['var_name'].update(focused_object_name)
            var_val_str = str(locals[focused_object_name])
            window['var_value'].update(var_val_str)
        




        # Import cv2 or matplotlib to show and display tensors 
        # that can be formatted as gray or RGB images
        if show_tensors:
            if hasattr(locals[event], "T"):
                # Is a torch or numpy array
                displayable = False
                is_torch_T = False
                if hasattr(locals[event], "device"):
                    is_torch_T = True

                tensor = locals[event]
                print(f"tensor: {event}")
                # is a torch Tensor
                # Check shape
                to_display = None
                if len(tensor.shape) == 2:
                    aspect_ratio = max(tensor.shape) / min(tensor.shape)
                    print(f"aspect ratio: {aspect_ratio}")
                    if aspect_ratio < 10:
                        print("probably reasonable to display")
                        if max(tensor.shape) < 352:
                            scale_factor = 352 / max(tensor.shape)
                            newshape = (int(tensor.shape[0] *scale_factor), int(tensor.shape[1] * scale_factor))
                            to_resize = None
                            if is_torch_T:
                                to_resize = tensor.unsqueeze(-1).cpu().detach().numpy()
                            else:
                                to_resize = tensor

                            resized = cv2.resize(to_resize, newshape, interpolation=cv2.INTER_NEAREST)
                            # cv2.imshow(f'Tensor-{event}', resized)
                            to_display = resized
                        else:
                            if is_torch_T:
                                to_display = tensor.unsqueeze(-1).cpu().detach().numpy()
                            else:
                                import numpy as np
                                to_display = np.expand_dims(tensor, -1)
                        displayable = True

                            # cv2.imshow(f'Tensor-{event}', tensor.unsqueeze(-1).cpu().detach().numpy())
                    #TODO: Display if enabled

                elif len(tensor.shape) >= 2:
                    print("at least two dimensional")
                    if 1 in tensor.shape or 3 in tensor.shape:
                        print("correct # of channels")
                        if tensor.shape[1] == 3 or tensor.shape[1] == 1:
                            #cv2.imshow(f'Tensor-{event}', tensor.squeeze(0).permute((1,2,0)).cpu().detach().numpy())
                            to_display = tensor.squeeze(0).permute((1,2,0)).cpu().detach().numpy()
                            displayable = True
                else:
                    continue
                
                # Select display method
                if True and displayable: 
                    import cv2
                    cv2.imshow(f'Tensor-{event}', to_display)

                print("")

        # for item in window.values():
        #     item.update(font='Helvetica ' + str(font_size))

    window.close()

if __name__ == '__main__':
    stack = inspect.stack(1)
    frame = stack[0]
    test = sg.Multiline("aaa")

    window = sg.Window('test', finalize=True)
    interact(locals=locals())