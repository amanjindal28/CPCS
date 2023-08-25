from fontio3 import fontedit
from fontio3.collectionedit import CollectionEditor as CE
from fontio3.fontmath import matrix
from fontio3.glyf import ttsimpleglyph, ttcompositeglyph, ttcomponents, ttcomponent
from fontio3.hmtx import MtxEntry
from fontio3.GSUB import ligature_glyphtuple
from fontio3.GSUB import ligature

def geteditorfrompath(path, ttcindex=None):
    if ttcindex is not None:
        editor = CE.frompath(path)[ttcindex]
    else:
        editor = fontedit.Editor.frompath(path)
    return editor

#write a function to update a list of unicodes to list of glyph ids using fontio3
def update_unicode_to_gid(unicodes, editor):
    umap = editor.cmap.getUnicodeMap()
    glyphIds = [umap.get(u) for u in unicodes]
    return glyphIds

def buildcompositeglyph(sourceeditor, desteditor, unicodes, **kwArgs):
    """ Build and return a TTCompsiteGlyph from desteditor from component gids,
    separated by width of space glyph from sourceeditor """
    glyphIds = update_unicode_to_gid(unicodes, sourceeditor)
    umap = sourceeditor.cmap.getUnicodeMap()
    spaceglyph = umap.get(0x0020)
    scalefactor = kwArgs.get('scalefactor', 1.0)
    spacewidth = int(round(sourceeditor.hmtx[spaceglyph].advance * scalefactor))
    newglyph = ttcompositeglyph.TTCompositeGlyph()
    xoffset = 0

    for c in glyphIds:
        cmpwidth = desteditor.hmtx[c].advance # note, *desteditor*

        if c != glyphIds[-1] and desteditor.reallyHas('kern'):
            nextglyph = glyphIds[glyphIds.index(c) + 1]
            for items in desteditor.kern:
                for key, value in items.items():
                    if key == (c, nextglyph):
                        cmpwidth += value
        tm = matrix.Matrix.forShift(xoffset, 0)
        newglyph.components.append(
            ttcomponent.TTComponent(glyphIndex=c, transformationMatrix=tm))
        xoffset += cmpwidth

    ngr = newglyph.recalculated(editor=desteditor)

    return ngr, xoffset

# write a function to create a copy of a font file ex. arial.ttf->tmp.ttf
# then create a sourceditor and a dest editor
# return the two editors
def copyfont(fontpath):
    srced = geteditorfrompath(fontpath)
    dested = srced.copy()
    return srced, dested

#write a function to load a font using fontio3 and create the sourceeditor
def update_font(fontpath):
    srced, dested = copyfont(fontpath)
    gl, adv = buildcompositeglyph(srced, dested, [0x0041, 0x0056],scalefactor=1)

    lsb = round(gl.bounds.xMin) if gl.bounds else 0
    maxglyph = dested.maxp.numGlyphs
    dested.glyf[maxglyph] = gl
    dested.hmtx[maxglyph] = MtxEntry(advance=adv, bearing=lsb)
    print('--------------------------')
    print(maxglyph)
    #add a ligature rule in the GSUB table to substitute [0x0041, 0x0056] to maxglyph
    GT = ligature_glyphtuple.Ligature_GlyphTuple
    objGT = GT([0x0043, 0x0041, 0x0054])
    objLig = ligature.Ligature({objGT: 97}, keyOrder=[objGT])

    #get the default LangSys for 'latn' script in GSUB
    defaultLangSys = dested.GSUB.scripts[b'latn'].defaultLangSys
    #TODO if not present prepare it

    if defaultLangSys.requiredFeature:
        allFeats = {defaultLangSys.requiredFeature}
    else:
        allFeats = set(defaultLangSys.optionalFeatures)

    for featTag in allFeats:
        feat = dested.GSUB.features[featTag]
        if feat.FeatureParams:
            feat.FeatureParams.ligatures.append(objLig)
        break
    

    dested.GSUB.featureVariations[0].featureTable.FeatureParams.ligatures.append(objLig)
    #add objLig to the first feature of feature list correspinding to 'latn' script in GSUB table
    dested.GSUB.scriptList['latn'].script.FeatureList.FeatureRecord[0].Feature.FeatureParams.ligatures.append(objLig)
    

    edrecalc = dested.recalculated(editor=dested)
    edrecalc.writeFont("temp.ttf")


#write the main function to call update_font with "UtahOTS.ttf"
def main():
    update_font("AdPro.ttf")

if __name__ == "__main__":
    main()       