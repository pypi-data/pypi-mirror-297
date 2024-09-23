import threading

class PluginBase:
    def __init__(self, main_module):
        self.main_module = main_module
        self.is_running = False        
        if hasattr(self.main_module, 'if_debug') and self.main_module.if_debug:
            print(f"[{type(self).__name__}] Plugin initialized.")        




    def start(self):
        threading.Thread(target=self.plugin_func).start()
        if hasattr(self.main_module, 'if_debug') and self.main_module.if_debug:
            print(f"[{type(self).__name__}] Plugin started.")

    def stop(self):
        self.is_running = False
        if hasattr(self.main_module, 'if_debug') and self.main_module.if_debug:
            print(f"[{type(self).__name__}] Plugin stopped.")


    def plugin_func(self, message):
        pass
        self.main_module.add_message(message)