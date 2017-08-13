<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

  <xsl:output method="text" indent="no"/>
  <xsl:strip-space elements="div"/>
  <xsl:template match="text()">
    <xsl:value-of select="replace(., '\s+', ' ')"/>
  </xsl:template>

  <xsl:template match="/">
    <xsl:apply-templates select="//body"/>
  </xsl:template>

  <xsl:template match="note" />

  <xsl:template match="p">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="milestone[@unit='para']">
    <xsl:apply-templates/>
    <xsl:text> </xsl:text>
  </xsl:template>

</xsl:stylesheet>
