rule fetch_db:
	output: "database/profiles.tar.gz"
	shell:
		"""
		wget -c https://www.genome.jp/ftp/db/kofam/profiles.tar.gz -O {output}	
		tar -xzvf database/profiles.tar.gz
		"""

rule fetch_ko:
	output: "database/ko_list"
	shell:
		"""
		wget -c https://www.genome.jp/ftp/db/kofam/ko_list.gz -O {output}
		gzip -d database/ko_list.gz
		"""
