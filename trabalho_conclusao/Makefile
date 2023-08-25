SCRIPTS_FOLDER=./etl_scripts
DATA_FOLDER=./data

etl/phase2/filter-train-sessions:
	python $(SCRIPTS_FOLDER)/cli.py filter-train-sessions \
	 --from-parquet-folder $(DATA_FOLDER)/transformed/train \
	 --to-parquet-file $(DATA_FOLDER)//transformed_train_data/sessions_with_more_than_2_clicks.parquet
