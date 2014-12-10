altium-lib-diff
===============
A tool for finding differences between Altium schematic and PCB library files.

```python3 libdiff.py old.SchLib new.SchLib
Added:
	 MAX5217GUA+
	 FDC6330L
	 ORNTA5000AT1
Removed:
Changed:
	 030-7328
		 changed FONTID: 4 -> 3
	 HCPL-181
		 changed FONTID: 4 -> 3
	 S1JB-13-F
		 changed FONTID: 3 -> 5
	 DIODE
		 changed FONTID: 3 -> 5
	 PINHEADER-1x1
		 changed FONTID: 4 -> 3
	 MOC3022S
		 changed FONTID: 4 -> 3
	 CRYSTAL
		 changed FONTID: 3 -> 5```

At the moment, this will only perform diffs for schematic library (.SchLib) files. Support for PCB libraries (.PcbLib) is being added.
