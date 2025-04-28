import subprocess

class cryptmgr:
    @staticmethod
    def keygen(argumento):
        result = subprocess.run(
            ['./keygen.sh', argumento],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Errore nell'eseguire il programma C: {result.stderr}")
        
        return result.stdout.strip()
