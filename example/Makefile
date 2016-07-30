.PHONY: setup-global setup-local backup_dashboard update_dashboard update_dashboards

setup-local:
	pip install -r requirements.txt

backup-dashboard:
	./backup_dashboard.sh $(id)

update-dashboard:
	./update_dashboard.sh $(file)

update-dashboards:
	./update_dashboards.sh
