from core.entities import Component, ServiceChain, Link, Edge, Node, Server
import numpy as np


class GridFactory(object):

    def __init__(self, data):
        self.data = data
        self.grid = None

    def create_grid(self):
        servers = self.__create_servers(self.data)
        components = self.__create_components(self.data)
        nodes = self.__create_nodes(self.data, servers)
        layout, edges = self.__create_layout(self.data, nodes)
        service_chains = self.__create_service_chains(self.data, components)
        links = self.__create_links(self.data, components)

        self.grid = Grid(servers, components, nodes, layout, service_chains, edges, links)

    def __create_servers(self, data):
        min_powers = data['P_min']
        max_powers = data['P_max']
        servers_available_resources = data['av']
        node_server_location = data['al']

        servers = []
        server_id = 0
        for min_power, max_power, available_resources in zip(min_powers, max_powers, servers_available_resources[0]):
            node_id = np.argmax(node_server_location[server_id])

            server = Server(
                server_id=server_id,
                node_id=node_id,
                min_power=min_power,
                max_power=max_power,
                resources_available=available_resources
            )

            server_id += 1
            servers.append(server)

        return np.array(servers)

    def __create_service_chains(self, data, components):
        service_chains = []
        for service_chain in data['sc']:
            service_chain_components = [components[int(component_id) - 1] for component_id in service_chain]
            service_chain = ServiceChain(service_chain_components)
            service_chains.append(service_chain)

        return service_chains

    def __create_components(self, data):
        resources_needed = data['req']
        processor_resources_needed = resources_needed[0]

        components = []
        for component_id, resources_needed in enumerate(processor_resources_needed):
            component = Component(resources_needed)
            components.append(component)

        return components

    def __create_nodes(self, data, servers):
        server_num = data['numServers']
        node_num = data['numNodes']
        power_usages = data['P']

        assert server_num == len(servers), 'Mismatch in server numbers.'

        nodes = []
        for node_id, power_usage in zip(range(node_num), power_usages):

            current_node_servers = [server for server in servers if server.node_id == node_id]
            node = Node(node_id, current_node_servers, power_usage)
            nodes.append(node)

        assert node_num == len(nodes), 'Mismatch in node numbers.'
        return nodes

    def __create_layout(self, data, nodes):
        edges = data['Edges']
        num_nodes = data['numNodes']

        layout = [[None] * num_nodes] * num_nodes
        edges = []
        for edge in edges:
            first_node_id, second_node_id, capacity, power_usage, delay = edge
            first_node_id, second_node_id = int(first_node_id) - 1, int(second_node_id) - 1

            first_node = nodes[first_node_id]
            second_node = nodes[second_node_id]

            new_edge = Edge(first_node, second_node, delay, capacity, power_usage)
            swaped_edge = Edge(second_node, first_node, delay, capacity, power_usage)
            edges.extend([new_edge, swaped_edge])

            self.__set_edges(first_node_id, second_node_id, layout, new_edge, swaped_edge, nodes)

        return layout, edges

    def __create_links(self, data, components):
        links = []
        for demand in data['VmDemands']:
            start_component_id, end_component_id, throughput = demand

            start_component = components[int(start_component_id) - 1]
            end_component = components[int(end_component_id) - 1]

            link = Link(start_component, end_component, throughput)
            links.append(link)

        return links

    def __set_edges(self, first_node_id, second_node_id, layout, new_edge, swaped_edge, nodes):
        layout[first_node_id][second_node_id] = new_edge
        layout[second_node_id][first_node_id] = swaped_edge

        nodes[first_node_id].add_adjacent_node(nodes[second_node_id])
        nodes[second_node_id].add_adjacent_node(nodes[first_node_id])

    def get_grid(self):
        assert self.grid is not None, 'You must call build_grid before this method!'

        return self.grid


class Grid(object):

    def __init__(self, servers, components, nodes, layout, service_chains, edges, links):
        self.servers = servers
        self.components = components
        self.nodes = nodes
        self.layout = layout
        self.service_chains = service_chains
        self.edges = edges
        self.links = links

    def is_active_edge(self, edge):
        assert isinstance(edge, Edge), 'Edge should be an instance of edge.'
        return any([service_chain.has_edge(edge) for service_chain in self.service_chains])

    def is_active_node(self, node):
        assert isinstance(node, Node), 'Node should be an instance of node.'

        active_edges = any([service_chain.has_node(node) for service_chain in self.service_chains])
        active_servers = any([server.is_active() for server in self.servers])
        return active_edges or active_servers