<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output indent="yes" method="xml" encoding="UTF-8" omit-xml-declaration="yes" />
  <xsl:template match="/">
     <xsl:apply-templates select="CGI_Result/motionDetectAlarm"/>
   </xsl:template>
   <xsl:template match="*">
     <xsl:choose>
        <xsl:when test="self::node()[node()=0]">"Sd card ok"</xsl:when>
        <xsl:when test="self::node()[node()=1]">"No SD card"</xsl:when>
        <xsl:when test="self::node()[node()=1]">"Sd card read only"</xsl:when>
     </xsl:choose>
  </xsl:template>
</xsl:stylesheet>