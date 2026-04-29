## Writing new code

1. **Specify the tech stack**
   Don’t ask AI to “build an app” in a vague way. Tell it the exact stack or approach, for example React, Vite, TypeScript, Tailwind, ShadCN, FastAPI, Postgres, etc. The speaker says this makes the first version easier to iterate on and signals to the AI that you have a concrete plan, which usually improves output quality. ([GitHub][1])

2. **Use popular technologies**
   Prefer widely used languages and frameworks such as JavaScript, Python, React, Postgres, FastAPI, Django, etc. The reason is simple: AI has seen far more examples of popular tools, so it is more likely to produce correct code. You also get more community help and examples online. ([GitHub][1])

3. **Design first, then ask AI to build**
   Before prompting, think through how the feature should actually work. The video gives the example of a search feature: should it search titles only, descriptions too, filters, sorting? If you skip this thinking, you may later say “it doesn’t work” when really the requirement was never clear. ([Lilys AI][2])

4. **Break things down into a task list**
   Instead of one broad request, give AI a numbered list of what the feature must do. For example: search titles and descriptions, filter by type, add sorting. This lets AI implement the pieces together instead of you repeatedly correcting one missing requirement at a time. ([GitHub][1])

5. **Find the right task scope**
   Don’t make tasks too tiny, like “move this icon” or “add padding,” because you waste time micromanaging. But don’t ask for an entire app in one go either. The right size is usually a complete feature or meaningful sub-feature, and you learn the balance through practice. ([GitHub][1])

6. **Use examples in prompts**
   Examples are often clearer than long descriptions. For a date-formatting function, showing input/output examples is better than trying to describe every formatting edge case in prose. AI tends to understand patterns well when it sees examples. ([GitHub][1])

7. **Provide sample code**
   When integrating a library or tool, give AI working sample code from docs or online examples. The speaker says this helps AI start from a proven base and makes the first attempt more likely to work. ([GitHub][1])

8. **Use `@Docs` and `@Web` context tools**
   If your AI coding tool supports documentation or web references, use them. This saves you from manually hunting docs and can improve the quality of generated solutions because AI has fresher, more relevant context. ([GitHub][1])

9. **Ask for security and performance checks**
   After AI builds a feature, ask whether it introduced security issues and whether the approach is efficient. You can include this in the original prompt or use it as an immediate follow-up. ([GitHub][1])

10. **Be proactive about hidden considerations**
    Ask whether there are best practices, constraints, or extra considerations for the feature or technology. This helps surface things you may not know to ask about yet. ([GitHub][1])

11. **Ask AI to write tests, or use TDD**
    You can ask AI to write tests after implementing a feature, or you can have it write tests first and then implement the feature against those tests. The speaker especially likes this with AI agents, because they can write tests, build the feature, run the tests, and iterate until everything passes. ([GitHub][1])

12. **Use AI to generate documentation**
    Have AI write README sections, comments, and end-user documentation. Since it has access to the code, it can often describe how the software works more precisely than a generic manual. ([GitHub][1])

13. **Use precise names**
    File, function, and class names matter because AI uses names to infer purpose. A CSV parser should be called something like `csvParser`, not a vague `dataParser`, otherwise AI may later cram unrelated parsing logic into the wrong place. ([GitHub][1])

## Modifying existing code

14. **Refactor and simplify regularly**
    Ask AI to split large or messy code into clearer files/functions. For example, extract CSV, XML, and PDF parsing into separate files. The point is to keep the codebase organized so AI can reason about it more easily. ([GitHub][1])

15. **Manage context carefully — the “golden rule”**
    The speaker says AI coding is largely about managing context. Too little context makes AI invent assumptions that don’t match your code. Too much context makes it confused, duplicate things, delete things, or miss the relevant part. ([GitHub][1])

16. **Tag the relevant files**
    When asking for changes, point AI to the exact files it needs and provide only the extra files that matter. This helps it write code that fits the existing architecture instead of guessing. ([GitHub][1])

17. **Keep files reasonably small**
    The guide recommends keeping files around 300 lines or less. The video explains the same idea through the opposite case: huge files, like thousands of lines, make it harder for AI to find the right code and can lead to duplicate functions or broken changes. ([GitHub][1])

18. **Remember the whole conversation becomes context**
    Long chats can become polluted with old decisions, outdated code, or irrelevant attempts. The AI may start referencing code that no longer exists or misunderstand the current state. ([GitHub][1])

19. **Start a new conversation for a new feature**
    When a new feature is not directly tied to the previous work, start fresh and include only the relevant files. This reduces context noise and helps the AI focus. ([GitHub][1])

20. **Tell AI what works and what still needs changing**
    After AI produces something partially correct, don’t only say “fix it.” Say what is working and what is not. This helps preserve the good parts while focusing the next attempt on the remaining issue. ([GitHub][1])

21. **Ask AI to find edge cases or bugs**
    Once the feature works, ask what edge cases are not handled or what issues remain. This pushes the AI into review mode and can make the product more robust. ([GitHub][1])

22. **Ask AI to review the code**
    After major changes, have AI review the implementation. The speaker stresses that you should still review the code yourself, especially to catch unnecessary, insecure, or unexpected implementation choices. ([GitHub][1])

23. **Ask AI what the current code does**
    Ask for a high-level or detailed explanation of a file/function. This can reveal details you missed and quickly show how the code fits into the broader codebase, especially when the code is large or unfamiliar. ([GitHub][1])

## Troubleshooting

24. **Be specific about what is and isn’t working**
    When debugging, describe the working part and the failing part. For example: “The button renders, but clicking it does nothing.” The more precise you are about where it fails, the faster AI can reason about the bug. ([GitHub][1])

25. **Share screenshots**
    For UI problems, screenshots can explain things words cannot. If you say “it’s not centered” or “it sticks to the top,” AI may lack visual context; a screenshot helps it understand the actual layout issue. ([GitHub][1])

26. **Share exact errors**
    Copy and paste the full error message or logs. The speaker says this often gives AI enough information to identify the source of the problem. ([GitHub][1])

27. **Use the Beaver Method**
    Ask AI to add logs throughout the process, run the app, then paste the generated logs back. This gives AI runtime context showing where the process breaks, instead of only seeing the final error. ([GitHub][1])

28. **Ask AI to explain the code during troubleshooting**
    If repeated fixes fail, ask AI to explain what the code is currently doing. Understanding the actual behavior may reveal that your mental model is wrong or that a case was not accounted for. ([GitHub][1])

29. **Ask for a radically different approach**
    The speaker’s “secret weapon” is asking AI to try a radically different approach. This can break loops where AI keeps making tiny adjustments to a flawed solution instead of stepping back and solving it another way. ([GitHub][1])

30. **Know when to stop asking AI and read the code yourself**
    AI can solve many problems quickly, so it’s worth letting it troubleshoot for a while. But if you’ve spent hours with logs and alternative approaches, you may need to inspect the code yourself, because the issue may be conceptual or caused by a technology limitation. ([GitHub][1])

## Learning to code with AI

31. **Tell AI you are new and ask it to keep things simple**
    If you don’t say this, AI may assume developer-level knowledge. Telling it you are learning helps it tailor explanations so you can actually understand them. ([GitHub][1])

32. **Ask for line-by-line explanations**
    Ask AI to explain code line by line or add comments. Repeating this helps you learn syntax, spot patterns, and understand why certain code looks different from previous examples. ([GitHub][1])

33. **Ask AI to explain technologies and concepts**
    Use AI to learn vocabulary and architecture, not only syntax. Ask what databases are, how full-stack apps work, what data types mean, or how a given technology relates to your project. This improves the quality of your future prompts too. ([GitHub][1])

34. **Ask AI how it would build something**
    For a feature or app idea, ask for the technical approach before coding. For example, a chat app could use a central server or peer-to-peer communication. Understanding these choices helps you prompt more clearly later. ([GitHub][1])

35. **Ask AI to show examples**
    Examples make abstract programming concepts concrete. The video mentions using examples for things like JavaScript functions and data types, which helps you connect theory to working code. ([GitHub][1])

36. **Tell AI what you understand and what is unclear**
    Explain your current understanding, then ask about the missing piece. AI can then connect the unknown concept to something you already know, which makes the explanation more useful. ([GitHub][1])

37. **Focus on core concepts, not just syntax**
    The final tip is to care less about memorizing exact syntax and more about understanding how software components fit together. The speaker points especially to understanding the layers of a full-stack application, because that bigger-picture knowledge makes you better at using AI to build real software. ([GitHub][1])

[1]: https://github.com/VoloBuilds/prompts/blob/main/ultimate-coding-prompt-guide.md "prompts/ultimate-coding-prompt-guide.md at main · VoloBuilds/prompts · GitHub"
[2]: https://lilys.ai/ko/notes/971942 "AI Coding 101: Ultimate Prompt Guide (37 tips)"
