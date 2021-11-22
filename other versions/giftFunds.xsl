<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
    <xsl:output method="text"/>
    <xsl:template match="collection">
        <xsl:text>MMS Id~Author~Author Name~Author Relator~Second Author Name~Second Author Relator~Corporate Author Name~Corporate Author Relator~Second Corporate Author Name~Second Corporate Author Relator~Title~First Place of Publication~First Publisher~First Published Year~Second Place of Publication~Second Publisher~Second Published Year&#xa;</xsl:text>
        <xsl:for-each select="record">
            <xsl:choose>
                <xsl:when test="controlfield[@tag = '001']">
                    <xsl:value-of select="controlfield[@tag = '001']"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '100']/subfield[@code = 'a']">
                    <xsl:for-each select="datafield[@tag = '100']/subfield[@code = 'a']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '100']/subfield[@code = 'a']">
                    <xsl:for-each select="datafield[@tag = '100']/subfield[@code = 'a']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '100']/subfield[@code = 'e']">
                    <xsl:for-each select="datafield[@tag = '100']/subfield[@code = 'e']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '110']/subfield[@code = 'a']">
                    <xsl:for-each select="datafield[@tag = '110']/subfield[@code = 'a']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '110']/subfield[@code = 'e']">
                    <xsl:for-each select="datafield[@tag = '110']/subfield[@code = 'e']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '700']/subfield[@code = 'a']">
                    <xsl:for-each select="datafield[@tag = '700']/subfield[@code = 'a']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '700']/subfield[@code = 'e']">
                    <xsl:for-each select="datafield[@tag = '700']/subfield[@code = 'e']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '710']/subfield[@code = 'a']">
                    <xsl:for-each select="datafield[@tag = '710']/subfield[@code = 'a']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '710']/subfield[@code = 'e']">
                    <xsl:for-each select="datafield[@tag = '710']/subfield[@code = 'e']">
                        <xsl:value-of select="."/>
                        <xsl:text>;&#160;</xsl:text>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '245']/subfield[@code = 'a']">
                    <xsl:value-of
                        select="normalize-space(datafield[@tag = '245']/subfield[@code = 'a'])"/>
                </xsl:when>
            </xsl:choose>

            <xsl:choose>
                <xsl:when test="datafield[@tag = '245']/subfield[@code = 'b']">
                    <xsl:text>&#160;</xsl:text>
                    <xsl:value-of
                        select="normalize-space(datafield[@tag = '245']/subfield[@code = 'b'])"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '260']/subfield[@code = 'a']">
                    <xsl:value-of select="datafield[@tag = '260']/subfield[@code = 'a']"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '260']/subfield[@code = 'b']">
                    <xsl:value-of select="datafield[@tag = '260']/subfield[@code = 'b']"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '260']/subfield[@code = 'c']">
                    <xsl:value-of select="datafield[@tag = '260']/subfield[@code = 'c']"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '264' and @ind2 = '1']/subfield[@code = 'a']">
                    <xsl:value-of
                        select="datafield[@tag = '264' and @ind2 = '1']/subfield[@code = 'a']"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '264' and @ind2 = '1']/subfield[@code = 'b']">
                    <xsl:value-of
                        select="datafield[@tag = '264' and @ind2 = '1']/subfield[@code = 'b']"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>~</xsl:text>
            <xsl:choose>
                <xsl:when test="datafield[@tag = '264' and @ind2 = '1']/subfield[@code = 'c']">
                    <xsl:value-of
                        select="datafield[@tag = '264' and @ind2 = '1']/subfield[@code = 'c']"/>
                </xsl:when>
            </xsl:choose>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
