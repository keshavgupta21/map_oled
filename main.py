from networkx.classes.multidigraph import MultiDiGraph
import osmnx as ox
import pickle
from PIL import Image

image_bbox = (42.4344, 42.2713, -70.8802, -71.2596) # boston
name = "boston"
# image_bbox = (21.2890, 21.0834, 81.1655, 81.5449) # bhilai
# name = "bhilai"
# graph = ox.graph_from_bbox(*image_bbox, truncate_by_edge=True)

# with open("graphs_{0}.pkl".format(name), "wb") as f:
#     pickle.dump(graph, f)

with open("graphs_{0}.pkl".format(name), "rb") as f:
   ref_graph = pickle.load(f)

road_types = {
    'trunk': (0.5, "#00ff00"),
    'tertiary': (0.2, "#007f00"),
    'secondary': (0.25, "#007f00"),
    'primary': (0.375, "#00ff00"),
    'residential': (0.1, "#007f00"),
    'track': (0, "#007f00"),
    'unclassified': (0, "#007f00"),
    'service': (0, "#007f00"),
    'footway': (0, "#007f00"),
    'primary_link': (0.5, "#007f00"),
    'secondary_link': (0.25, "#007f00"),
    'tertiary_link': (0.2, "#007f00"),
    'motorway': (1, "#00ff00"),
}
cumulative_image = None

for cur_rt in road_types:
    edge_linewidth, edge_color = road_types[cur_rt]
    if edge_linewidth > 0:
        with open("graphs_{0}.pkl".format(name), "rb") as f:
            wrk_graph = pickle.load(f)
        for (u, v, k, d) in ref_graph.edges(keys = True, data = True):
            hw = d.get("highway", None)
            if type(hw) is not list and hw != cur_rt:
                if wrk_graph.has_edge(u, v, k):
                    wrk_graph.remove_edge(u, v, k)
        ox.plot_graph(wrk_graph, node_size = 0, 
            bbox = image_bbox,
            show = False, save = True, 
            filepath = "images/" + cur_rt + ".png", dpi = 600,
            bgcolor = "#000000", edge_color = edge_color,
            edge_linewidth = edge_linewidth)
        img = Image.open("images/" + cur_rt + ".png")
        if cumulative_image is None:
            cumulative_image = Image.new("RGBA", img.size)
        cumulative_image = Image.blend(cumulative_image, img, 0.5)
        cumulative_image = Image.eval(cumulative_image, lambda x: x*2)
cumulative_image.save("final.png")
    