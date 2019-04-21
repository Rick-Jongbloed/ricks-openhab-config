<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output indent="yes" method="xml" encoding="UTF-8" omit-xml-declaration="yes" />
  <xsl:template match="/">
     <xsl:apply-templates select="CGI_Result/ntpState"/>
   </xsl:template>
   <xsl:template match="*">
     <xsl:choose>
        <xsl:when test="self::node()[node()=0]">"Disabled"</xsl:when>
        <xsl:when test="self::node()[node()=1]">"Update success"</xsl:when>
        <xsl:when test="self::node()[node()=2]">"Update fail"</xsl:when>
     </xsl:choose>
  </xsl:template>
</xsl:stylesheet>