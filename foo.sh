          if [[ "aas" == "windows-2022" ]]; then
            for %i in (dist\*.tar.gz) do python -m pip install %i
          else
            python -m pip install dist/*.tar.gz
          fi