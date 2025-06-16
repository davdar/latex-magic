s/⇡→\*/\\overrightarrow /g
s/⇡→/\\vec /g
s/⇡~\*/\\widetilde /g
s/⇡~/\\tilde /g
s/⇡\^\*/\\widehat /g
s/⇡\^/\\hat /g
s/⇡-\*/\\overline /g
s/⇡-/\\bar /g
s/⇡\./\\dot /g
s/⇡‥/\\ddot /g
s/⇡…/\\dddot /g
s/⇡u/\\breve /g
s/⇡v/\\check /g
s/⇡o/\\mathring /g
s/⇡w\*/\\overbrace/g
s/⇡e\*/\\overbracket/g

s/⇣-\*/\\underline /g
s/⇣w\*/\\underbrace/g
s/⇣e\*/\\underbracket/g

s/⇡/\\oversetOn /g
s/⇣/\\undersetOn /g

s/“/``/g
s/”/''/g

s/❬/\\label{/g
s/❭/}/g
s/⦉/~\\ref{/g
s/⦊/}/g
s/⦇/\\eqref{/g
s/⦈/}/g
s/⟬𝔞/\\citeauthor{/g
s/⟬/\\citet{/g
s/⟭/}/g
s/⦅𝔶/~\\citeyearpar{/g
s/⦅/~\\citep{/g
s/⦆/}/g

# ⟪ text color + textrm    ⟫
# ⦑ syntax color + texttt  ⦒
# ⸨ math color + math mode ⸩

# ‹  textrm     ›
# «  textit     »
# ⋖  texttt     ⋗ 
# «* textbf    *»
# ⦗  textsc     ⦘
# ❪  math mode  ❫

s/⟪/\\daraisTEXT{/g
s/⟫/}/g

s/⸨/\\daraisMATH{/g
s/⸩/}/g

s/⦑/\\daraisSTAX{/g
s/⦒/}/g

s/‹/{\\daraisModeRM{/g
s/›/}}/g
s/«\*/{\\daraisModeBF{/g
s/\*»/}}/g
s/«/{\\daraisModeIT{/g
s/»/}}/g
s/⋖/{\\daraisModeTT{/g
s/⋗/}}/g
s/⦗/{\\daraisModeSC{/g
s/⦘/}}/g
s/❪/{\\daraisModeMM{/g
s/❫/}}/g
s/⪡/{\\verb/g
s/⪢/}/g

s/𝔠/\\inlinecode/g

s/⌄/\\footnote/g

s/𝑚𝑐(.)(.)/\\multicolumn{\1}{\2}/g

s/Z⁃//g

s/I⁅/\\begin{itemize}\\item /g
s/I⁃/\\item /g
s/I⁆/\\end{itemize}/g

s/J⁅/\\begin{parlist}\\item /g
s/J⁃/\\item /g
s/J⁆/\\end{parlist}/g

s/E⁅/\\begin{enumerate}\\item /g
s/E⁃/\\item /g
s/E⁆/\\end{enumerate}/g

s/Q⁅/\\begin{quote}/g
s/Q⁆/\\end{quote}/g

s/F⁅\[H\]/\\begin{figure}[H]/g
s/F⁅/\\begin{figure}/g
s/F⁆/\\end{figure}/g

s/D⁅/\\begin{framed}/g
s/D⁆/\\end{framed}/g

s/M⁅/\\begingroup\\color{\\colorMATH}\\begin{gather*}/g
s/M⁃/\\cr /g
s/M⁆/\\end{gather*}\\endgroup/g

s/X⁅/\\begin{tabularx}{\\linewidth}{>{\\centering\\arraybackslash\\(}X<{\\)}}/g
s/X⁃/\\cr /g
s/X⁆/\\end{tabularx}/g

s/Aː\[t\]/\\begin{array}[t]{/g
s/Aː\[b\]/\\begin{array}[b]{/g
s/Aː/\\begin{array}{/g
s/A⁅/}/g
s/A⁃/\\cr /g
s/A⁆/\\end{array}/g

s/Tː\[t\]/\\begin{tabular}[t]{/g
s/Tː\[b\]/\\begin{tabular}[b]{/g
s/Tː/\\begin{tabular}{/g
s/T⁅/}/g
s/T⁃/\\cr /g
s/T⁆/\\end{tabular}/g

s/P⁅/\\begingroup\\color{\\colorMATH}\\begin{mathpar}/g
s/P⁃/\\and/g
s/P◘/\\\\/g
s/P⁆/\\end{mathpar}\\endgroup/g

s/Rː\*/\\inferrule*[/g
s/Rː\[l\]/\\inferrule*[left=/g
s/Rː\[r\]/\\inferrule*[right=/g
s/Rː/\\inferrule*[lab=/g
s/R⁅/]{/g
s/R⁃/\\\\/g
s/R◘/\\\\\\\\/g
s/----[-]*/}{/g
s/R⁆/}/g

s/B⁅/\\begingroup\\color{\\colorTEXT}\\boxed{\\begingroup\\color{\\colorMATH}/g
s/B⁆/\\endgroup}\\endgroup/g

s/V⁅/\\begin{verbatim}/g
s/V⁆/\\end{verbatim}/g

s/⁅⁅/\\parbox{\\linewidth}{/g
s/⁆⁆/}/g

s/‘/\\left/g
s/’/\\right/g
s/⫾/␣\\middle|␣/g

s/⧼/\&{}/g
s/⧽/{}\&/g

s/␣/\\hspace*{0.33em}/g
s/꘍/\\hspace*{0.66em}/g
s/␠/\\hspace*{1.00em}/g
s/⩊/\\hfill\\hspace{0pt}/g

s/‗/\\underline{\\hspace{0.66em}}/g

s/⸤/_{/g
s/⸥/}/g
s/⸢/^{/g
s/⸣/}/g
