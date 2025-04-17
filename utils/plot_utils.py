import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def bar_chart(labels, counts, xlabel, ylabel, title, color="skyblue"):
    """
    Static matplotlib chart (non-GUI).
    """
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def gui_bar_chart(tk_root, labels, counts, xlabel, ylabel, title, color="skyblue"):
    """
    Draws a matplotlib bar chart inside a Tkinter window.
    Returns a tuple: (figure, axis, canvas)
    """
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    canvas.get_tk_widget().pack(padx=20, pady=15)

    pos = range(len(labels))
    ax.bar(pos, counts, color=color)
    ax.set_xticks(pos)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=11)
    ax.set_xlabel(xlabel, fontsize=13)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.set_title(title, fontsize=15, weight="bold")
    fig.tight_layout()
    canvas.draw()

    return fig, ax, canvas
