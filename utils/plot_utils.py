# Import matplotlib for creating visualizations
import matplotlib.pyplot as plt


def bar_chart(labels, counts, xlabel, ylabel, title, color="skyblue"):
    """
    Plots a bar chart using the provided labels and values.

    Args:
        labels (list): Categories or labels to display on the x-axis.
        counts (list): Corresponding numerical values for each label on the y-axis.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        title (str): Title of the chart.
        color (str, optional): Color of the bars. Defaults to "skyblue".
    """
    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Create a bar chart with the specified color
    plt.bar(labels, counts, color=color)

    # Set axis labels and chart title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Adjust layout to prevent clipping of labels
    plt.tight_layout()

    # Display the chart
    plt.show()
