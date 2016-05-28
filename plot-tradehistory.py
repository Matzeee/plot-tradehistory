# -*- coding: utf-8 -*-


def evaluate(intial_balance=0, normalise=100, open_browser=False):
    """
    Unofficial: Evaluates and plots tradehistory[…].csv from Ayondo® TradeHub®

    Parameters
    ----------

    intial_balance:
        Balace before first "Bank Wire".
        Useful if export does not start from the outset.

    normalise:
        Trend for one deposit of chosen amount at the outset.

    open_browser:
        Open "chart.html" in browser or just save it.
    """

    import pandas as pd
    result = 0

    def find_latest():
        import glob
        from datetime import date

        names = ["transactionhistory_????????_to_????????.csv",
                 "transaktionshistorie_????????_bis_????????.csv",
                 "transactionhistory_????????_hasta_????????.csv",
                 "transactionhistory_????????_para_????????.csv"]

        dir_list = []
        for name in names:
            dir_list += glob.glob(name)

        latest = {"date": date(1, 1, 1)}

        for item in dir_list:
            try:
                year = int(item[-8:-4])
                month = int(item[-10:-8])
                day = int(item[-12:-10])

                itemdate = date(year, month, day)

                if itemdate >= latest["date"]:
                    latest["date"] = itemdate
                    latest["filename"] = item
            except:
                pass

        try:
            if __name__ == "__main__":
                print("Newest csv:", latest["filename"])
            return(latest["filename"])
        except:
            import sys
            sys.exit("Could not find a matching csv!")

    def import_Data(csvfile):

        colnames = ["ID", "Time", "Product", "Type", "Amount", "Balance"]

        with open(csvfile, 'r') as f:
            return pd.read_csv(f, sep=",", decimal=".",
                               index_col=False, skiprows=1,
                               parse_dates=[1], dayfirst=True, names=colnames)

    def evaluate(paid_in=intial_balance, normalised=normalise):
        nonlocal data

        data.sort_values(by="Time", inplace=True, kind="mergesort")
        # is almost perfectly sorted

        line = pd.DataFrame({"Normalised": normalised, "Paid-in": paid_in}, index=[0])
        data = pd.concat([line, data])
        data.reset_index(drop=True, inplace=True)

        for row, col in data.iterrows():
            if (row > 0):
                Amount = data.at[row, "Amount"]
                Balance = data.at[row, "Balance"]

                if data.at[row, "Type"] == "Bank Wire":
                    data.at[row, "Normalised"] = data.at[row-1, "Normalised"]
                    paid_in += Amount
                    data.at[row, "Paid-in"] = paid_in

                else:
                    data.at[row, "Normalised"] = data.at[row-1, "Normalised"] * (1+Amount/(Balance-Amount))
                    data.at[row, "Paid-in"] = paid_in

        balance = data.columns.get_loc("Balance")
        paid_in = data.columns.get_loc("Paid-in")
        nonlocal result
        result = data.iat[-1, balance] - data.iat[-1, paid_in]

    def export():
        nonlocal data

        import bokeh.charts as bch
        # from bokeh.models import HoverTool, GlyphRenderer
        bch.output_file("Chart.html")

        data = data.iloc[1:, :]

        TOOLS = "pan,wheel_zoom,box_zoom,crosshair,resize,reset"  # ,hover,box_select"

        title = "History (total result: {} €)".format(result)
        cols = ["Paid-in", "Balance", "Normalised"]

        tsline = bch.TimeSeries(data,
                                x="Time",
                                y=cols,
                                title=title, tools=TOOLS,
                                ylabel='Euro', legend=True,
                                width=1250, height=550)

        if open_browser:
            bch.show(bch.vplot(tsline))
        else:
            bch.save(bch.vplot(tsline))

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.style.use('ggplot')

        data.plot(x="Time", y=["Normalised", "Balance", "Paid-in"])
        plt.savefig("data.pdf")

    data = import_Data(find_latest())
    evaluate()

    if __name__ == "__main__":
        print("Result:", result)

    export()

if __name__ == "__main__":
    evaluate(intial_balance=0, normalise=100, open_browser=True)
