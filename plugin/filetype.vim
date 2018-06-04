if exists("did_load_filetypes")
  finish
endif
augroup filetypedetect
      au! BufNewFile,BufRead email*.txt,email*.xml,*.html setf html
      au! BufNewFile,BufRead styles,nstyles setf xml
      au! BufNewFile,BufRead survey.xml setf xml
      au! BufNewFile,BufRead *.txt,*.dat,*.csv setf csv
augroup END
