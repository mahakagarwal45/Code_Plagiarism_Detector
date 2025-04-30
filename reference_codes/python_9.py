def root_item_selected(self, item):
        """Root item has been selected: expanding it and collapsing others"""
        if self.show_all_files:
            return
        for root_item in self.get_top_level_items():
            if root_item is item:
                self.expandItem(root_item)
            else:
                self.collapseItem(root_item)