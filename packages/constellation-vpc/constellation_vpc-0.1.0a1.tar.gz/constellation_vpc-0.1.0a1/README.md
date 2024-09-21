# constallation-vpc
## Version 0.1.0a1
### **<span style="color:red;">Warning | Do Not Use for anything important</span>**
**The version _0.1.0a1_ is a package from the alpha stages and also pre-release** and has **undergone very minimal testing.** This version was built on `08/08/2024` Please use something more modern and closer to latest as this package is not secure for any actual use and its release serves archival means. 

***
### Changelist
- #### **<span style="color:red;">0.1.0a0</span>**
  - Created _vpc base class for AWS VPC operations
  - Created and implemented a Subnet Object Based class
  - Created ErrorHandler to convert AWS CLI Errors to Python Exceptions
- #### **<span style="color:red;">0.1.0a1</span>**
  - ##### <span style="color:#73ff98;">Added Error Handling for the following AWS CLI Errors
    - ###### <span style="color:#73ceff;"> **InvalidSubnet**
      - ID.NotFound
      - ZoneMismatch
      - InUse
      - Association
      - DependentService
      - Attachment
    - ###### <span style="color:#73ceff;"> AccessDenied
    - ###### <span style="color:#73ceff;"> AuthFailure
    - ###### <span style="color:#73ceff;"> RequestLimitExceeded
    - ###### <span style="color:#73ceff;"> ThrottlingException
    - ###### <span style="color:#73ceff;"> ResourceNotFoundException
    - ###### <span style="color:#73ceff;"> InvalidParameterValue
    - ###### <span style="color:#73ceff;"> ServiceUnavailable
    - ###### <span style="color:#73ceff;"> InternalFailure
    - ###### <span style="color:#73ceff;"> ValidationException
    - ###### <span style="color:#73ceff;"> InvalidClientTokenId
    - ###### <span style="color:#73ceff;"> OptInRequired