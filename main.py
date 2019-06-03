import osmnx as ox
import pickle
from PIL import Image

# FILENAME = "map.osm"
# graph = ox.graph_from_file(FILENAME)

# with open("graphs.pkl", "wb") as f:
    # pickle.dump(graph, f)

with open("graphs.pkl", "rb") as f:
   ref_graph = pickle.load(f)

road_types = {
    'trunk': 1,
    'tertiary': 0.4,
    'secondary': 0.5,
    'primary': 0.75,
    'residential': 0.075,
    'track': 0.1,
    'unclassified': 0,
    'service': 0,
    'footway': 0,
    'secondary_link': 0,
    'tertiary_link': 0
}
cumulative_image = Image.new("RGBA", (1674, 2547))

for cur_rt in road_types:
    with open("graphs.pkl", "rb") as f:
        wrk_graph = pickle.load(f)
    for (u, v, k, d) in ref_graph.edges(keys = True, data = True):
        hw = d.get("highway", None)
        if type(hw) is not list and hw != cur_rt:
            wrk_graph.remove_edge(u, v, k)
    ox.plot_graph(wrk_graph, node_size = 0, 
        bbox = (21.4092, 20.9591, 81.5346, 81.2176), 
        margin = 0, show = False, save = True, 
        filename = cur_rt, dpi = 240, 
        fig_height = 16, fig_width = 9, 
        bgcolor = "#000000", edge_color = "#ffffff",
        edge_linewidth = road_types[cur_rt])
    img = Image.open("images/" + cur_rt + ".png")
    cumulative_image = Image.blend(cumulative_image, img, 0.5)
    cumulative_image = Image.eval(cumulative_image, lambda x: x*2)
cumulative_image.save("final.png")
    