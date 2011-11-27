
%global parent plexus
%global subname maven-plugin

%global maven_settings_file %{_builddir}/%{name}/settings.xml

Name:           %{parent}-%{subname}
Version:        1.3.8
Release:        6
Summary:        Plexus Maven plugin
License:        MIT
Group:          Development/Java
URL:            http://plexus.codehaus.org/

# svn export \
#   http://svn.codehaus.org/plexus/archive/plexus-maven-plugin/tags/plexus-maven-plugin-1.3.8
# tar czf plexus-maven-plugin-1.3.8-src.tar.xz plexus-maven-plugin-1.3.8
Source0:        %{name}-%{version}-src.tar.gz

Patch0:         %{name}-doxia.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven2-common-poms >= 1.0
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  plexus-appserver >= 1.0-0.a5.3
BuildRequires:  plexus-cdc >= 1.0-0.8.a14
BuildRequires:  plexus-container-default
BuildRequires:  plexus-runtime-builder >= 1.0-0.a9.2

Requires:       maven2
Requires:       maven2-common-poms >= 1.0
Requires:       plexus-appserver >= 1.0-0.a5.3
Requires:       plexus-cdc >= 1.0-0.8.a14
Requires:       plexus-container-default
Requires:       plexus-runtime-builder >= 1.0-0.a9.2
Requires:       maven-shared-reporting-impl

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
Plexus Maven Plugin helps create plexus component descriptions
from within Maven.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1

%build
mvn-rpmbuild install javadoc:javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 target/*.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{parent}/%{subname}.jar
%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/plexus
%{_mavenpomdir}/*pom
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

