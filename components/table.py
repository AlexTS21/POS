from scripts.database import DataBase
import ttkbootstrap as ttkb

class customTable:

    def __init__(self, data, frame, fields, acciones=None, filters=None, orderFilters=None):
        """
        Creates a table inside a frame

        Parameters:
            data (list): List of dictionaries of the shown data
            frame (frame): Where the table will be placed
            fields (dict): Fields names and anchor
            acciones (dict): Campos con una funcion
            orderFilters (List): Fields to order in abc or cba
            fiters (dic): key column and value a list of values the field can take


        Returns:
            bool: True if at least one row was updated, False otherwise.
        """
        self.data= data
        print(data[0].keys())
        print(fields.keys())
        scrollbar = ttkb.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        #Filters
        self.orderFiltersValue = None
        self.filtersValue = None

        if orderFilters or filters:
            filter_frame = ttkb.Frame(frame)
            filter_frame.pack( fill='x', padx=(0, 30), pady=(0,10))  # Estira horizontalmente

        #Filtros de orden
        if orderFilters:
            orderFrame = ttkb.Frame(filter_frame)
            orderFrame.grid(column=0, row=0, sticky="e")
            ttkb.Label(orderFrame, text="Ordenar por:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5)
            self.orderFiltersValue = {}
            self.var_sort = ttkb.StringVar(value="0")
            for i, o in enumerate(orderFilters):
                ttkb.Radiobutton(orderFrame, text=f"{o} ↑", variable=self.var_sort, value=str(i*2), bootstyle="info", command=self.aplicar_filtros).grid(row=0, column=(i+1)*2, padx=5)
                ttkb.Radiobutton(orderFrame, text=f"{o} ↓", variable=self.var_sort, value=str(i*2 +1), bootstyle="info", command=self.aplicar_filtros).grid(row=0, column=(i+1)*2+1, padx=5)
                self.orderFiltersValue[str(i*2)] = f"{o} ↑"
                self.orderFiltersValue[str(i*2 + 1)] = f"{o} ↓"

        if filters:
            sortFrame = ttkb.Frame(filter_frame)
            sortFrame.grid(column=1, row=0, sticky="e")
            ttkb.Label(sortFrame, text="Filtrar por:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5)
            self.filtersValue = {}
            self.var_ord = ttkb.StringVar(value="0")
            ttkb.Radiobutton(sortFrame, text="Todos", variable=self.var_ord, value="0", bootstyle="info", command=self.aplicar_filtros).grid(row=0, column=1, padx=5)

            i = 1
            for k, values in filters.items():
                for v in values:
                    ttkb.Radiobutton(sortFrame, text=v, variable=self.var_ord, value=str(i), bootstyle="info", command=self.aplicar_filtros).grid(row=0, column=i+2, padx=5)
                    self.filtersValue[str(i)] = [k, v]
                    i+=1
                    
                

        print(self.filtersValue)
        print(self.orderFiltersValue)
        # Add treeview
        self.tree = ttkb.Treeview(
            frame,
            columns=list(fields.keys()),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=10
        )
        scrollbar.config(command=self.tree.yview)

        for k, v in fields.items():
            self.tree.heading(k, text=k)
            self.tree.column(k, width=v, anchor='center')
        
        self.tree.pack(fill='both', expand=True)
        self.load_on_table(self.data)

    def load_on_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for d in data:
            self.tree.insert(
                '', 'end',
                values=(
                    list(d.values())
                )
            )
        return
    
    def aplicar_filtros(self):
        if self.filtersValue:
            value = self.var_ord.get()
            if value == "0":
                dataAUX = self.data
            else:
                dataAUX = [d for d in self.data if d.get(self.filtersValue[value][0]) == self.filtersValue[value][1]]
        else:
            dataAUX = self.data
        if self.orderFiltersValue:
            value = self.var_sort.get()
            if self.orderFiltersValue[value][-1] == "↑":
                data = sorted(dataAUX, key=lambda x: x[self.orderFiltersValue[value][:-2]])
            elif self.orderFiltersValue[value][-1] == "↓":
                data = sorted(dataAUX, key=lambda x: x[self.orderFiltersValue[value][:-2]], reverse=True)
       
        self.load_on_table(data)
        return
    

