" decipher_clips.vim - A collection of functions to help create Decipher surveys
"
" Place this script and the accompanying deciphervimclips directory in .vim/plugin
"
" See README.rst for additional information.
"
" Maintainer: Ryan Scarbery <ryan.scarbery@gmail.com>
" Version: 0.1.2

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')


if !has('python') && !has('python3')
   " exit if python is not available.
   finish
endif

function! s:UsingPython3()
  if has('python3')
    return 1
  endif
  return 0
endfunction

let s:using_python3 = s:UsingPython3()
let s:python_until_eof = s:using_python3 ? "python3 << EOF" : "python << EOF"
let s:python_until_eof_range = s:using_python3 ? "'<,'>python3 << EOF" : "'<,'>python << EOF"
let s:python_command = s:using_python3 ? "py3 " : "py "


" Setup
exec s:python_until_eof
import os
import sys
import vim

#from urllib import quote
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = os.path.normpath(os.path.join(plugin_root_dir, 'deciphervimclips'))
sys.path.insert(0, python_root_dir)
import commands
import deciphervimclips
EOF

" Normal Mode Mappings
nmap <leader>ss  <Esc>ggVG:call CleanUp()<CR><Esc>:call NewSurvey()<CR>
nmap <leader>mo  <Esc>:call MakeOrs()<Esc>
nmap <leader>ju  <Esc>:call Justify()<CR>
nmap <leader>sr  <Esc>:call SwitchRating()<CR>
nmap <leader>dif <Esc>:call Vimdiff()<CR>
nmap <leader>no  <Esc>:call CleanNotes()<CR>
nmap <leader>ee  <Esc>i exclusive="1" randomize="0"<Esc>
nmap <leader>rr  <Esc>i randomize="0"<Esc>
nmap <leader>oe  <Esc>i open="1" openSize="25" randomize="0"<Esc>
nmap <leader>aa  <Esc>i aggregate="0" percentages="0"<Esc>
nmap <leader>oo  <Esc>i optional="1"<Esc>
nmap <leader>dev <Esc>i where="execute"<Esc>
nmap <leader>sh  <Esc>i shuffle="rows"<Esc>
nmap <leader>su  <Esc>o<suspend/><Esc>
nmap <leader>br  <Esc>i<br/><br/><Esc>
nmap <leader>mb  <Esc>i<br><br><Esc>
nmap <leader>nu  <Esc>:.,$s'\v(^\d+) '\1. 'gc<CR>
nmap <leader>le  <Esc>:.,$s'\v(^[A-Z]+) '\1. 'gc<CR>
nmap <leader>va  <Esc>:call Validate()<Esc>
nmap <leader>cb  <Esc>:call CommentBlocks()<Esc>


" Visual Mode Mappings
vmap <leader>ro  <Esc>:call Rows()<CR>
vmap <leader>co  <Esc>:call Cols()<CR>
vmap <leader>ch  <Esc>:call Choice()<CR>
vmap <leader>ra  <Esc>:call Rates()<CR>
vmap <leader>mr  <Esc>:call MakeRadio()<CR>
vmap <leader>mc  <Esc>:call MakeCheckbox()<CR>
vmap <leader>ms  <Esc>:call MakeSelect()<CR>
vmap <leader>mn  <Esc>:call MakeNumber()<CR>
vmap <leader>mf  <Esc>:call MakeFloat()<CR>
vmap <leader>mt  <Esc>:call MakeText()<CR>
vmap <leader>ma  <Esc>:call MakeTextarea()<CR>
vmap <leader>mh  <Esc>:call MakeHTML()<CR>
vmap <leader>mv  <Esc>:call MakeRating()<CR>
vmap <leader>re  <Esc>:call Resource()<CR>
vmap <leader>mg  <Esc>:call MakeGroups()<CR>
vmap <leader>ne  <Esc>:call MakeNets()<CR>
vmap <leader>na  <Esc>:call NoAnswer()<CR>
vmap <leader>ca  <Esc>:call Case()<CR>
vmap <leader>avl <Esc>:call AddValuesLow()<CR>
vmap <leader>avh <Esc>:call AddValuesHigh()<CR>
vmap <leader>ag  <Esc>:call AddGroups()<CR>
vmap <leader>aa  <Esc>:call AddAlts()<CR>
vmap <leader>qc  <Esc>:call CommentQuestion()<CR>
vmap <leader>es  <Esc>:call Escape()<Esc>
vmap <leader>hc  <Esc>:call HTMLComment()<CR>
vmap <leader>me  <Esc>:call MakeExtras()<CR>
vmap <leader>qs  <Esc>:call SpaceQuote()<Esc>
vmap <leader>st  <Esc>:call Strip()<CR>
vmap <leader>sw  <Esc>:call Switcher()<CR>
vmap <leader>qu  <Esc>:call URLQuote()<Esc>
vmap <leader>cl  <Esc>:call CleanUp()<CR>
vmap <leader>hr  <Esc>:call HRef()<CR>
vmap <leader>ml  <Esc>:call MailLink()<CR>
vmap <leader>as  <Esc>:call AttrSpacing()<CR>


function! NewSurvey()
exec s:python_until_eof
try:

    commands.NewSurvey()

except Exception as e:
    print(e)
EOF
endfunction


function! CleanUp()
exec s:python_until_eof_range
try:

    commands.CleanUp()

except Exception as e:
    print(e)
EOF
endfunction


function! AttrSpacing()
exec s:python_until_eof_range
try:

    vim.current.range[:] = deciphervimclips.clean_attribute_spacing(vim.current.range[:])

except Exception as e:
    print(e)
EOF
endfunction


function! Rows()
exec s:python_until_eof_range
try:

    commands.Rows()

except Exception as e:
    print(e)
EOF
endfunction


function! Cols()
exec s:python_until_eof_range
try:

    commands.Cols()    

except Exception as e:
    print(e)
EOF
endfunction


function! Choice()
exec s:python_until_eof_range
try:

    commands.Choice() 

except Exception as e:
    print(e)
EOF
endfunction


function! Rates()
exec s:python_until_eof_range
try:

    commands.Rates()

except Exception as e:
    print(e)
EOF
endfunction


function! Case()
exec s:python_until_eof_range
try:

    commands.Case()

except Exception as e:
    print(e)
EOF
endfunction


function! NoAnswer()
exec s:python_until_eof_range
try:

    commands.NoAnswer()

except Exception as e:
    print(e)
EOF
endfunction


function! Resource()
exec s:python_until_eof_range
try:

    commands.Resource()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeRadio()
exec s:python_until_eof_range
try:

    commands.MakeRadio()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeCheckbox()
exec s:python_until_eof_range
try:

    commands.MakeCheckbox()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeSelect()
exec s:python_until_eof_range
try:

    commands.MakeSelect()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeNumber()
exec s:python_until_eof_range
try:

    commands.MakeNumber()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeFloat()
exec s:python_until_eof_range
try:

    commands.MakeFloat()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeText()
exec s:python_until_eof_range
try:

   commands.MakeText()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeTextarea()
exec s:python_until_eof_range
try:

    commands.MakeTextarea()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeHTML()
exec s:python_until_eof_range
try:

    commands.MakeHTML()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeRating()
exec s:python_until_eof_range
try:

    commands.MakeRating()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeNets()
exec s:python_until_eof_range
try:

    commands.MakeNets()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeGroups()
exec s:python_until_eof_range
try:

    commands.MakeGroups()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeExtras()
exec s:python_until_eof_range
try:

    commands.MakeExtras()

except Exception as e:
    print(e)
EOF
endfunction


function! MakeOrs()
exec s:python_until_eof
try:

    commands.MainMakeOrs()

except Exception as e:
    print(e)
EOF
endfunction


function! AddValuesLow()
exec s:python_until_eof_range
try:

    commands.AddValuesLow()

except Exception as e:
    print(e)
EOF
endfunction


function! AddValuesHigh()
exec s:python_until_eof_range
try:

    commands.AddValuesHigh()

except Exception as e:
    print(e)
EOF
endfunction


function! Switcher()
exec s:python_until_eof_range
try:

    commands.Switcher()

except Exception as e:
    print(e)
EOF
endfunction


function! SwitchRating()
exec s:python_until_eof
try:

    commands.SwitchRating()

except Exception as e:
    print(e)
EOF
endfunction


function! AddGroups()
exec s:python_until_eof_range
try:

    commands.AddGroups()

except Exception as e:
    print(e)
EOF
endfunction


function! CommentQuestion()
exec s:python_until_eof_range
try:

    commands.CommentQuestion()

except Exception as e:
    print(e)
EOF
endfunction


function! HTMLComment()
exec s:python_until_eof_range
try:

    commands.HTMLComment()

except Exception as e:
    print(e)
EOF
endfunction


function! AddAlts()
exec s:python_until_eof_range
try:

    commands.AddAlts()

except Exception as e:
    print(e)
EOF
endfunction


function! Validate()
exec s:python_until_eof
try:
    """
    TODO Remove macro lines @foo bar=baz
    TODO Validate xml
    TODO Search for optional without <validate/>
    """
    raise NotImplementedError("XXX TODO external validate module")

except Exception as e:
    print(e)
EOF
endfunction


function! Escape()
exec s:python_until_eof_range
try:

    vim.current.range[:] = [line.replace('<', '&lt;').replace('>', '&gt;') for line in vim.current.range[:]]

except Exception as e:
    print(e)
EOF
endfunction


function! URLQuote()
exec s:python_until_eof_range
try:

    commands.URLQuote()

except Exception as e:
    print(e)
EOF
endfunction


function! SpaceQuote()
exec s:python_until_eof_range
try:

    vim.current.range[:] = [line.replace(' ', '&#32;') for line in vim.current.range[:]]

except Exception as e:
    print(e)
EOF
endfunction


function! MailLink()
exec s:python_until_eof_range
try:
    def MailLink(selection):
        return '<a href="mailto:{email}">{email}</a>'.format(email=selection)

    if vim.eval('visualmode()') == u'\x16':
        raise NotImplementedError("Visual Block Mode Not Supported")
    start = vim.current.buffer.mark('<')
    end   = vim.current.buffer.mark('>')
    before, inside, after = deciphervimclips.get_visual_selection(vim.current.range[:], start, end)
    vim.current.range[:] = (before + MailLink(inside) + after).split('\n')

except Exception as e:
    print(e)
EOF
endfunction


function! HRef()
exec s:python_until_eof_range
try:
    def HRef(selection):
        return '<a href="{selection}">{selection}</a>'.format(selection=selection)

    if vim.eval('visualmode()') == u'\x16':
        raise NotImplementedError("Visual Block Mode Not Supported")
    start = vim.current.buffer.mark('<')
    end   = vim.current.buffer.mark('>')
    before, inside, after = deciphervimclips.get_visual_selection(vim.current.range[:], start, end)
    vim.current.range[:] = (before + HRef(inside) + after).split('\n')

except Exception as e:
    print(e)
EOF
endfunction


function! Strip()
exec s:python_until_eof_range
try:

    commands.Strip()

except Exception as e:
    print(e)
EOF
endfunction


function! Justify()
exec s:python_until_eof
try:

    commands.Justify()

except Exception as e:
    print(e)
EOF
endfunction


function! CleanNotes()
exec s:python_until_eof
try:

    commands.CleanNotes()

except Exception as e:
    print(e)
EOF
endfunction


function! Vimdiff()
exec s:python_until_eof
"""
Split buffer by blank lines and open in vimdiff
"""
try:
    import tempfile
    from subprocess import Popen, PIPE

    PROGRAM = 'gvimdiff'

    vbuffer = '\n'.join(vim.current.buffer[:])

    parts = vbuffer.split('\n\n')

    files = []

    for part in parts:
        tmp = tempfile.NamedTemporaryFile()
        tmp.write(part)
        tmp.flush()
        files.append(tmp)

    cmd = [PROGRAM] + [f.name for f in files]

    Popen(cmd, stdout=PIPE).wait()

except Exception as e:
    print(e)
EOF
endfunction


function! CommentBlocks()
exec s:python_until_eof
"""
Add <!-- EO block --> style comments
to the end of blocks for easier navigation
of nested block trees
"""
try:
    def CommentBlocks(lines):
        from xml import sax
        import re


        EOBTemplate = '<!-- EO {label} -->'  # END OF BLOCK Template


        class BlockCommentHandler(sax.ContentHandler):
            def __init__(self, documentLines):
                sax.ContentHandler.__init__(self)
                self.documentLines = documentLines
                self.blocks = []
                self.lineCount = 0  # number of lines added for offset

            def startElement(self, name, attrs):
                if name == 'block':
                    self.blocks.append(attrs['label'])

            def endElement(self, name):
                if name == 'block':
                    lineNo = self._locator.getLineNumber()
                    label = self.blocks.pop()
                    comment = EOBTemplate.format(label=label)
                    eobIndex = lineNo + self.lineCount
                    eobLine = self.documentLines[eobIndex]
                    if re.search(EOBTemplate.format(label='.*'), eobLine):
                        return  # already commented
                    self.documentLines.insert(eobIndex, comment)
                    self.lineCount += 1

        sh = BlockCommentHandler(lines)
        doc = sax.parseString('\n'.join(lines), sh)

        return sh.documentLines

    vim.current.buffer[:] = CommentBlocks(vim.current.buffer[:])

except Exception as e:
    print(e)
EOF
endfunction



