
format:
	black --ipynb --exclude='.py' ./notebooks/ ./trabalho_conclusao/  \
	&& black --exclude='.ipynb' ./notebooks/etl ./trabalho_conclusao/etl

