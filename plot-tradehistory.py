# -*- coding: utf-8 -*-


def evaluate(initial_balance=0, initial_bonus=0,
             bonus_real=0, normalise=100, open_browser=False):
    """
    Unofficial: Evaluates and plots transactionhistory[…].csv from Ayondo® TradeHub®

    Parameters
    ----------

    intial_balance:
        Balace before first "Bank Wire" in given history.
        Useful if export does not start from the outset.

    initial_bonus:
        Bonus before first "Bonus" in given history.
        Useful if export does not start from the outset.

    bonus_real:
        Bonus that will not be removed if money is paid out;
        enough spread has been generated.

    normalise:
        Trend for one deposit of chosen amount at the outset.

    open_browser:
        Open "chart.html" in browser or just save it.
    """

    import pandas as pd
    result = 0

    diff = bonus_real - initial_bonus
    if diff > 0:
        bonus_real = diff
        bonus = 0
    else:
        bonus = - diff
        bonus_real = 0

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

    def evaluate(paid_in=initial_balance, normalised=normalise):
        nonlocal data, result, bonus, bonus_real

        data.sort_values(by="Time", inplace=True, kind="mergesort")
        # is almost perfectly sorted

        line = pd.DataFrame(
                {"Normalised": normalised, "Paid-in": paid_in}, index=[0])

        data = pd.concat([line, data])
        data.reset_index(drop=True, inplace=True)

        for row, col in data.iterrows():
            if (row > 0):
                amount = data.at[row, "Amount"]
                balance = data.at[row, "Balance"]

                if data.at[row, "Type"] == "Bank Wire":
                    paid_in += amount

                elif data.at[row, "Type"] == "Bonus":
                    diff = bonus_real - amount
                    if diff > 0:
                        bonus = 0
                        bonus_real = diff
                    else:
                        bonus -= diff
                        bonus_real = 0

                else:
                    normalised = normalised * (1+amount/(balance-amount))

                data.at[row, "Paid-in"] = paid_in
                data.at[row, "Normalised"] = normalised
                data.at[row, "Total Result"] = balance - paid_in - bonus
                data.at[row, "Total Result incl Bonus"] = balance - paid_in

        balance = data.columns.get_loc("Balance")
        paid_in = data.columns.get_loc("Paid-in")
        result = data.iat[-1, balance] - data.iat[-1, paid_in] - bonus

    def export():
        nonlocal data

        import bokeh.charts as bch
        from bokeh.layouts import column
        # from bokeh.models import HoverTool, GlyphRenderer
        bch.output_file("Chart.html")

        data = data.iloc[1:, :]

        # TOOLS = "pan, wheel_zoom, box_zoom, crosshair, resize, reset "# , hover"

        title = "History (total result: {0:.2f} €)".format(result)
        if bonus > 0:
            title = title[:-1] + ", excluding Bonus: {0:.2f} €)".format(bonus)

        cols = ["Paid-in", "Balance", "Normalised", "Total Result"]
        if bonus > 0:
            cols = ["Paid-in", "Balance", "Normalised",
                    "Total Result incl Bonus", "Total Result"]

        tsline = bch.TimeSeries(data,
                                x="Time",
                                y=cols,
                                title=title,  # tools=TOOLS,
                                ylabel='Euro', legend=True,
                                width=1250, height=550)
        """
        from bokeh.models import HoverTool
        hover = HoverTool(
            tooltips=[
                ("index", "$index"),
                ("(x,y)", "($x, $y)"),
                ("desc", "$balance"),
                # ("test", data.iloc["$index", 4])
            ]
        )

        tsline.add_tools(hover)
        """

        if open_browser:
            bch.show(column(tsline))
        else:
            bch.save(column(tsline))

        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.style.use('ggplot')

        data.plot(x="Time", y=cols)
        plt.savefig("Chart.pdf")

    data = import_Data(find_latest())
    evaluate()

    if __name__ == "__main__":
        toprint = "Total result: {0:.2f} €".format(result)
        if bonus > 0:
            toprint += "\nExcluding Bonus: {0:.2f} €".format(bonus)
        try:
            print(toprint)
        except UnicodeEncodeError:
            print(toprint.replace("€", "EUR"))

    export()

if __name__ == "__main__":
    evaluate(initial_balance=0, normalise=1000,
             initial_bonus=0, bonus_real=0, open_browser=False)
