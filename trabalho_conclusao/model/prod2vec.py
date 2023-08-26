import tensorflow as tf


class Prod2Vec(tf.keras.Model):
    def __init__(
        self,
        num_products,
        embedding_dim,
    ):
        """
        Args:
            * num_products (int): Number of products in the dataset.
            * embedding_dim (int): Dimension of the embedding vector.
        """
        super(Prod2Vec, self).__init__()
        self.target_embedding = tf.keras.layers.Embedding(
            num_products,
            embedding_dim,
            input_length=1,
            name="prod2vec_embedding",
        )

        # self.context_embedding =

        self.dot = tf.keras.layers.Dot(axes=1)
