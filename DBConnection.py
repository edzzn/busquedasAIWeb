import psycopg2 
import Node

class Connection:
    def __init__(self):
        self.DB_HOST = "ec2-54-204-14-96.compute-1.amazonaws.com"
        self.DB_DB = "d68lno2cct2tpd"
        self.DB_USER = "nmipfnmxbjfosa"
        self.DB_PASSWORD = "40a0f08bfad570064c89ba5e3862fe0e2322dabaaaf09aec9460cf9a1afdbc0c"
        self.creation_commands = [
            """
            CREATE TABLE nodes
            (
                node_id SERIAL PRIMARY KEY,
                node_name VARCHAR(255) NOT NULL,
                node_peso INTEGER,        
                CONSTRAINT "Name_unique" UNIQUE (node_name)
            )
            WITH (
                OIDS = FALSE
            )
            """,
            """
            CREATE TABLE edges
            (
                edge_id SERIAL PRIMARY KEY,
                parent_id INTEGER NOT NULL,
                child_id INTEGER NOT NULL, 
                edge_peso INTEGER,        
                CONSTRAINT parent_child_unique UNIQUE (parent_id, child_id),
                CONSTRAINT "child_FK" FOREIGN KEY (child_id)
                    REFERENCES nodes (node_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION,
                CONSTRAINT "parent_FK" FOREIGN KEY (parent_id)
                    REFERENCES nodes (node_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            )
            WITH (
                OIDS = FALSE
            )
            """
           ]

    def create_tables(self):
        conn = None

        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(host=self.DB_HOST ,database=self.DB_DB , user=self.DB_USER , password=self.DB_PASSWORD)
            cur = conn.cursor()

            for command in self.creation_commands:
                cur.execute(command)

            cur.close()

            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def insert_node(self, node):
        sql =  """INSERT INTO nodes(node_name, node_peso)
                 VALUES(%s, %s) RETURNING node_id;"""

        conn = None
        node_id = None
        node_name = node.name
        node_peso = node.value
        try:
            conn = psycopg2.connect(host=self.DB_HOST ,database=self.DB_DB , user=self.DB_USER , password=self.DB_PASSWORD)

            cur = conn.cursor()

            cur.execute(sql, (node_name, node_peso,))

            # get the generated node id
            node_id = cur.fetchone()[0]

            conn.commit()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return node_id

    def get_nodes(self):
        conn = None
        nodes = []
        try:
            conn = psycopg2.connect(host=self.DB_HOST ,database=self.DB_DB , user=self.DB_USER , password=self.DB_PASSWORD)
            cur = conn.cursor()
            cur.execute("SELECT node_name, node_peso FROM nodes ORDER BY node_name")
            rows = cur.fetchall()

            for row in rows:
                nodes.append(Node.Node(row[0][0], row[0][1]))

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return nodes 

    def get_edges(self, nodes):
        conn = None
        edges = []
        try:
            conn = psycopg2.connect(host=self.DB_HOST ,database=self.DB_DB , user=self.DB_USER , password=self.DB_PASSWORD)
            cur = conn.cursor()
            print(f"nodes: {nodes}")

            for node in nodes:
                # print(f"node: {node}")
                cur.execute(f"SELECT node_id FROM nodes WHERE node_name = '{node.name}'")
                parent_id = cur.fetchone()[0]
                # print(f"parent_id: {parent_id}")

                cur.execute(f"SELECT child_id FROM edges WHERE parent_id = '{parent_id}'")

                rows = cur.fetchall()
                # print(f"rows: {rows}")

                for row in rows:
                    cur.execute(f"SELECT node_name FROM nodes WHERE node_id = '{row[0]}'")
                    child_name = cur.fetchone()[0]
                    print(f"child_name: {child_name}")
                    child_node = list(filter(lambda child: child.name == child_name, nodes))
                    print(f"child_node: {child_node}")

                    node.addChildren([child_node[0]])
                    # print(f"node: {node}")

                    edges.append( (node, child_node[0]) )
                # print(f"edges: {edges}")
                
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        # print(nodes)
        # print(edges)
        
        return nodes, edges

    def insert_edge(self, parent_node, child_node):
        sql =  """INSERT INTO edges(parent_id, child_id, edge_peso)
                 VALUES(%s, %s, %s) RETURNING edge_id;"""

        conn = None
        edge_id = None
        parent_id = None
        child_id = None
        edge_peso = parent_node.pesos[child_node]
        parent_name = parent_node.name
        child_name = child_node.name
        try:
            conn = psycopg2.connect(host=self.DB_HOST ,database=self.DB_DB , user=self.DB_USER , password=self.DB_PASSWORD)

            cur = conn.cursor()

            cur.execute(f"SELECT node_id FROM nodes WHERE node_name = '{parent_name}'")
            parent_id = cur.fetchone()[0]
            cur.execute(f"SELECT node_id FROM nodes WHERE node_name = '{child_name}'")
            child_id = cur.fetchone()[0]

            cur.execute(sql, (parent_id, child_id, edge_peso))

            # get the generated node id
            edge_id = cur.fetchone()[0]

            conn.commit()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return edge_id

if __name__ == '__main__':
    conn = Connection()
    conn.create_tables()
