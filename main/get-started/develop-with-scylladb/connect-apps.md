# Connect an Application

To connect your application to ScyllaDB, you need to:

1. [Install the relevant driver](https://docs.scylladb.com/stable/get-started/develop-with-scylladb/install-drivers.md)
   for your application language.

   This step involves setting up a driver that is compatible with ScyllaDB.
   The driver acts as the link between your application and ScyllaDB, enabling
   your application to communicate with the database.
2. Modify your application code to connect the driver.

   The following is some boilerplate code to help familiarize yourself with
   connecting your application with the ScyllaDB driver. For a detailed
   walkthrough of building a fictional media player application with code
   examples, please see our
   [Getting Started tutorial](https://cloud-getting-started.scylladb.com/stable/getting-started.html).

Rust

```rust
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
```

Go

```go
func main() {
    cluster := gocql.NewCluster("localhost")

    cluster.Authenticator = gocql.PasswordAuthenticator{Username: "scylla", Password: "your-awesome-password"}

          session, err := gocqlx.WrapSession(cluster.CreateSession())

          if err != nil {
                    panic("Connection fail")
          }
 }
```

Java

```java
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
```

Python

```python
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
cluster = Cluster(
    contact_points=[
        "localhost",
    ],
    auth_provider=PlainTextAuthProvider(username='scylla', password='your-awesome-password')
)
```

JavaScript

```javascript
const cluster = new cassandra.Client({
    contactPoints: ["localhost", ...],
    localDataCenter: 'your-data-center',
    credentials: {username: 'scylla', password: 'your-awesome-password'},
    // keyspace: 'your_keyspace' // optional
})
```
