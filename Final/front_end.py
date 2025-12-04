import social_graph

if __name__ == "__main__":

    # intro
    print("=====Network Analysis=====")
    print("The dataset the programmer used is from SNAP (Facebook Network)")

    # loading the network / graph
    print("Now Loading the Graph / Network...")
    G, featnames, feature_order, features, ego_features, circles, ego_node_id = social_graph.build_graph(0)
    print("Finished!")

    # prompt user for visualizing the graph
    while True:

        want_visualized = input("Do you want to see the Graph with true circles? (y/n)")

        if want_visualized == "y":
            social_graph.visualization(G, circles, ego_node_id)
            break
        elif want_visualized == "n":
            break
        else:
            continue

    # prompt user for visualizing the graph with louvain detection
    while True:

        want_visualized_louvain = input("Do you want to see the Graph with louvain communities? (y/n)")

        if want_visualized_louvain == "y":
            social_graph.visualization_louvain(G, ego_node_id)
            break
        elif want_visualized_louvain == "n":
            break
        else:
            continue

    partition = social_graph.circle_detection(G)
    
    # prompt user and see if he / she want to check the summary of feature name in certain circle / community
    while True:

        type_summary_featname = input("Check the community / circle feature name summary (louv / cir / n for quit): ")

        if type_summary_featname == "louv":

            id_summary = int(input("Input community id: "))

            top_feats = social_graph.summarize_community_features(G, 
            community_id = id_summary, 
            method = type_summary_featname, 
            partition = partition, 
            circles = circles,
            features = features,
            featnames = featnames,
            feature_order = feature_order,
            top_k = 10)

            print(top_feats)

            break
        
        elif type_summary_featname == "cir":

            id_summary = int(input("Input circle id: "))

            top_feats = social_graph.summarize_community_features(G, 
            community_id = id_summary, 
            method = type_summary_featname, 
            partition = partition, 
            circles = circles,
            features = features,
            featnames = featnames,
            feature_order = feature_order,
            top_k = 10)

            print(top_feats)

            break

        elif type_summary_featname == "n":

            break

        else:

            continue

    # prompt user for querying
    print("Here are some nodes in the Graph")
    print(social_graph.show_node(G, 5))

    # prompt user for checking the node attributes
    while True:

        query_node = input("Which node do you want to query (n for quit): ")

        if query_node.isdigit():

            if int(query_node) in list(G.nodes()):

                social_graph.node_information(G, int(query_node), featnames, feature_order)

                again = input("Do you want to query again? (y/n) ")

                if again == "y":
                    continue
                elif again == "n":
                    break
                else:
                    continue

        elif query_node == "n":
            break

        else:
            continue
    
    # ending
    print("Thank you for trying the network analysis!")
