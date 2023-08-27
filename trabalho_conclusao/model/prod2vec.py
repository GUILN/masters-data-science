import tensorflow as tf


class Prod2Vec(tf.keras.Model):
    def __init__(
        self,
        num_products: int,
        embedding_dim: int,
        num_negative_samples=3,
    ):
        """
        Args:
            * num_products (int): Number of products in the dataset.
            * embedding_dim (int): Dimension of the embedding vector.
            * num_negative_samples (int): Number of negative samples to be used in the loss function.
        """
        super(Prod2Vec, self).__init__()
        self.target_embedding = tf.keras.layers.Embedding(
            num_products,
            embedding_dim,
            input_length=1,
            name="prod2vec_embedding",
        )

        self.context_embedding = tf.keras.layers.Embedding(
            num_products,
            embedding_dim,
            input_length=num_negative_samples + 1,
        )

    def call(self, pair: tuple):
        """
        Args:
            * pair (tuple): Tuple containing the target and context products.
        """
        target, context = pair
        if len(target.shape) == 2:
            target = tf.squeeze(target, axis=1)
        word_embedding = self.target_embedding(target)
        context_embedding = self.context_embedding(context)
        dots = tf.einsum("be,bce->bc", word_embedding, context_embedding)
        return dots
