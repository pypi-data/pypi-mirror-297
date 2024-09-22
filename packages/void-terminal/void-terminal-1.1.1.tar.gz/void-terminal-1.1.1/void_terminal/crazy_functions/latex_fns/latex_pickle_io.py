import pickle


class SafeUnpickler(pickle.Unpickler):

    def get_safe_classes(self):
        from void_terminal.crazy_functions.latex_fns.latex_actions import LatexPaperFileGroup, LatexPaperSplit
        from void_terminal.crazy_functions.latex_fns.latex_toolbox import LinkedListNode
        # Define allowed security classes
        safe_classes = {
            # Add other secure classes here
            'LatexPaperFileGroup': LatexPaperFileGroup,
            'LatexPaperSplit': LatexPaperSplit,
            'LinkedListNode': LinkedListNode,
        }
        return safe_classes

    def find_class(self, module, name):
        # Only allow specific classes to be deserialized
        self.safe_classes = self.get_safe_classes()
        match_class_name = None
        for class_name in self.safe_classes.keys():
            if (class_name in f'{module}.{name}'):
                match_class_name = class_name
        if module == 'numpy' or module.startswith('numpy.'):
            return super().find_class(module, name)
        if match_class_name is not None:
            return self.safe_classes[match_class_name]
        # If trying to load unauthorized class，Then throw an exception
        raise pickle.UnpicklingError(f"Attempted to deserialize unauthorized class '{name}' from module '{module}'")

def objdump(obj, file="objdump.tmp"):

    with open(file, "wb+") as f:
        pickle.dump(obj, f)
    return


def objload(file="objdump.tmp"):
    import os

    if not os.path.exists(file):
        return
    with open(file, "rb") as f:
        unpickler = SafeUnpickler(f)
        return unpickler.load()
