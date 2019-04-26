<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output indent="yes" method="xml" encoding="UTF-8" omit-xml-declaration="yes" />
  <xsl:template match="/">
     <xsl:apply-templates select="CGI_Result/infraLedState"/>
   </xsl:template>
   <xsl:template match="*">
     <xsl:choose>
        <xsl:when test="self::node()[node()=1]">ON</xsl:when>
        <xsl:when test="self::node()[node()=0]">OFF</xsl:when>
        <xsl:otherwise><xsl:value-of select="@service"/></xsl:otherwise>
     </xsl:choose>
  </xsl:template>
</xsl:stylesheet>