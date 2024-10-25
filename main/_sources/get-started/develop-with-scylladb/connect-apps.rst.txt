=======================
Connect an Application
=======================

To connect your application to ScyllaDB, you need to:

#. :doc:`Install the relevant driver </get-started/develop-with-scylladb/install-drivers>` 
   for your application language.
 
   This step involves setting up a driver that is compatible with ScyllaDB. 
   The driver acts as the link between your application and ScyllaDB, enabling 
   your application to communicate with the database.

#. Modify your application code to connect the driver. 

   The following is some boilerplate code to help familiarize yourself with 
   connecting your application with the ScyllaDB driver. For a detailed 
   walkthrough of building a fictional media player application with code 
   examples, please see our 
   `Getting Started tutorial <https://cloud-getting-started.scylladb.com/stable/getting-started.html>`_.

.. tabs::

  .. group-tab:: Rust

    .. code-block:: rust

      use anyhow::Result;in various languages
      use scylla::{Session, SessionBuilder};
      use std::time::Duration;
      #[tokio::main]
      async fn main() -> Result<()> {
          let session: Session = SessionBuilder::new()
              .known_nodes(&[
                  "localhost",
              ])
              .connection_timeout(Duration::from_secs(30))
              .user("scylla", "your-awesome-password")
              .build()
              .await
              .unwrap();

          Ok(())
      }

  .. group-tab:: Go

    .. code-block:: go

      func main() {
          cluster := gocql.NewCluster("localhost")

          cluster.Authenticator = gocql.PasswordAuthenticator{Username: "scylla", Password: "your-awesome-password"}

	        session, err := gocqlx.WrapSession(cluster.CreateSession())

	        if err != nil {
		          panic("Connection fail")
	        }
       }



  .. group-tab:: Java

    .. code-block:: java

      import com.datastax.driver.core.Cluster;  
      import com.datastax.driver.core.PlainTextAuthProvider;  
      import com.datastax.driver.core.Session;  
  
      class Main {  
  
          public static void main(String[] args) {  
          Cluster cluster = Cluster.builder()  
              .addContactPoints("localhost")  
              .withAuthProvider(new PlainTextAuthProvider("scylla", "your-awesome-password"))  
              .build();  
    
          Session session = cluster.connect();  
    
          }  
      }

  .. group-tab:: Python

    .. code-block:: python

      from cassandra.cluster import Cluster 
      from cassandra.auth import PlainTextAuthProvider
      cluster = Cluster(
          contact_points=[
              "localhost",
          ],
          auth_provider=PlainTextAuthProvider(username='scylla', password='your-awesome-password')
      )

  .. group-tab:: JavaScript

    .. code-block:: javascript

      const cluster = new cassandra.Client({
          contactPoints: ["localhost", ...],
          localDataCenter: 'your-data-center', 
          credentials: {username: 'scylla', password: 'your-awesome-password'},
          // keyspace: 'your_keyspace' // optional
      })
