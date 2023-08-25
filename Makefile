
format:
	black --ipynb --exclude='.py' ./notebooks/ ./trabalho_conclusao/  \
	&& black --exclude='.ipynb' ./notebooks/ ./trabalho_conclusao/

