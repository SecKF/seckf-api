##Description:

The product exposes sensitive information to an actor that is not explicitly authorized to have access to that information.

There are many different kinds of mistakes that introduce information exposures. The severity of the error can range widely, depending on the context in which the product operates, the type of sensitive information that is revealed, and the benefits it may provide to an attacker. Some kinds of sensitive information include: private, personal information, such as personal messages, ficial data, health records, geographic location, or contact details system status and environment, such as the operating system and installed packages business secrets and intellectual property network status and configuration the product's own code or internal state metadata, e.g. logging of connections or message headers indirect information, such as a discrepancy between two internal operations that can be observed by an outsider Information might be sensitive to different parties, each of which may have their own expectations for whether the information should be protected. These parties include: the product's own users people or organizations whose information is created or used by the product, even if they are not direct product users the product's administrators, including the admins of the system(s) and/or networks on which the product operates the developer Information exposures can occur in different ways: the code explicitly inserts sensitive information into resources that are made accessible to unauthorized actors a different weakness or mistake inadvertently makes the sensitive information available, such as a web script error revealing the full system path of the program

##Mitigation:


PHASE:Architecture and Design:STRATEGY:Separation of Privilege:
Compartmentalize the system to have safe areas where trust boundaries can be unambiguously drawn. Do not allow sensitive data to go outside of the trust boundary and always be careful when interfacing with a compartment outside of the safe area. Ensure that appropriate compartmentalization is built into the system design and that the compartmentalization serves to allow for and further reinforce privilege separation functionality. Architects and designers should rely on the principle of least privilege to decide when it is appropriate to use and to drop system privileges.

