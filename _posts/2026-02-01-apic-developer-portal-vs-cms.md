---
layout: post
date: 2026-02-01 01:00:00
categories: APIConnect
title: "Choosing Between API Connect Developer Portal and CMS Portal: A Practical Guide"
author: ["ChrisPhillips","ChrisDudley"]
draft: true
---

When implementing IBM API Connect, one of the key decisions you'll face is choosing between the Developer Portal and the CMS Portal. While both serve the purpose of exposing your APIs to developers, they offer significantly different levels of customization and require different skill sets. This guide will help you understand the differences and choose the right option for your needs.

<!--more-->

## Understanding the Two Portal Options

IBM API Connect offers two distinct portal solutions, each designed for different use cases and organizational requirements:

### Developer Portal: Configuration-Based Customization

The Developer Portal is designed for teams who want powerful customization capabilities without writing code. It provides a streamlined, configuration-driven approach to portal management.

**Key Characteristics:**
- **No-Code Customization**: All customization is done through the admin UI
- **Built-in Flexibility**: Create custom asset types and add custom fields through configuration
- **Styling Options**: Apply custom CSS for branding and visual customization
- **Web Components**: Support for custom web components for advanced UI needs

**Important Limitation**: You cannot write actual code to customize the Developer Portal - all customization is configuration-based.

### CMS Portal: Full Drupal Ecosystem Access

The CMS Portal provides complete access to the Drupal ecosystem, enabling virtually unlimited customization possibilities for organizations with the technical resources to support it.

**Key Characteristics:**
- **Full Drupal Access**: Complete access to Drupal's extensive module ecosystem
- **Code-Level Customization**: Write custom code to achieve any desired functionality
- **Maximum Flexibility**: Implement complex, unique requirements that go beyond standard portal features
- **Technical Expertise Required**: Requires Drupal development skills and ongoing maintenance


## Detailed Comparison

### Customization Capabilities

**Developer Portal:**
```
✓ Admin UI configuration
✓ Custom asset types
✓ Custom fields
✓ Custom CSS styling
✓ Custom web components
✗ Custom code development
✗ Direct Drupal module access
```

**CMS Portal:**
```
✓ Everything in Developer Portal
✓ Custom code development
✓ Full Drupal module ecosystem
✓ Database-level customization
✓ Custom PHP development
✓ Advanced integrations
```


### Use Case Scenarios

**Choose Developer Portal When:**

1. **Standard Requirements**: Your portal needs align with common API portal use cases
2. **Limited Technical Resources**: You don't have dedicated Drupal developers
3. **Rapid Deployment**: You need to get a portal up and running quickly
4. **Minimal Maintenance**: You want IBM to handle updates and security patches
5. **Configuration is Sufficient**: Your customization needs can be met through admin UI settings

**Example Scenario:**
> A mid-sized company wants to expose their APIs with custom branding, specific content types for API documentation, and integration with their SSO system. The Developer Portal's configuration options and custom CSS can handle all these requirements without code.

**Choose CMS Portal When:**

1. **Unique Requirements**: You need functionality that goes beyond standard portal capabilities
2. **Drupal Expertise Available**: You have experienced Drupal developers on staff
3. **Complex Integrations**: You need deep integration with enterprise systems
4. **Custom Workflows**: You require specialized approval processes or content workflows
5. **Full Control Needed**: You need complete control over every aspect of the portal

**Example Scenario:**
> An enterprise organization needs to integrate their portal with multiple internal systems, implement complex approval workflows, create custom reporting dashboards, and provide specialized developer onboarding experiences. The CMS Portal's full Drupal access enables all these custom requirements.

## Making the Decision

### Decision Framework

Ask yourself these questions:

1. **Do we have Drupal development expertise in-house?**
   - No → Developer Portal
   - Yes → Consider CMS Portal

2. **Can our requirements be met through configuration?**
   - Yes → Developer Portal
   - No → CMS Portal

3. **Are we prepared to maintain Drupal core updates?**
   - No → Developer Portal
   - Yes → CMS Portal is viable

4. **Do we need custom code-level functionality?**
   - No → Developer Portal
   - Yes → CMS Portal

5. **What's our timeline?**
   - Quick deployment → Developer Portal
   - Extended development acceptable → CMS Portal

### Cost Considerations

**Developer Portal:**
- Lower initial setup cost
- Minimal ongoing maintenance cost
- No specialized staff required
- Predictable operational costs

**CMS Portal:**
- Higher initial development cost
- Ongoing maintenance and update costs
- Requires specialized Drupal developers
- Variable operational costs based on customization complexity

## Migration Path

It's important to note that while you can start with the Developer Portal and later migrate to CMS Portal if needs evolve, the reverse migration is more complex. Consider your long-term requirements when making the initial decision.

## Best Practices

### For Developer Portal Users:

1. **Maximize Configuration**: Explore all configuration options before considering CMS Portal
2. **Use Custom CSS Effectively**: Leverage CSS for branding and visual customization
3. **Plan Asset Types**: Design custom asset types to match your content structure
4. **Document Customizations**: Keep clear documentation of all configuration changes

### For CMS Portal Users:

1. **Establish Update Procedures**: Create a process for applying Drupal core updates
2. **Security First**: Implement security scanning and patch management
3. **Code Standards**: Follow Drupal coding standards for maintainability
4. **Testing Environment**: Maintain separate dev/test/prod environments
5. **Backup Strategy**: Implement comprehensive backup and recovery procedures

## Additional Resources

- [Developer Portal Documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=using-developer-portal)
- [CMS Portal Documentation](https://www.ibm.com/docs/en/api-connect/software/12.1.0?topic=portal-using-cms)

## Conclusion

The choice between Developer Portal and CMS Portal ultimately depends on your organization's technical capabilities, customization requirements, and maintenance capacity:

- **Choose Developer Portal** for standard requirements, rapid deployment, and minimal maintenance
- **Choose CMS Portal** for unique requirements, complex customizations, and when you have Drupal expertise

Most organizations will find the Developer Portal meets their needs while providing significant customization flexibility without the overhead of managing a full Drupal installation. Reserve the CMS Portal for scenarios where you truly need code-level customization and have the resources to support it.

---

*Have questions about which portal option is right for your organization? Feel free to reach out or leave a comment below.*