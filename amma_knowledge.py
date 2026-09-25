AMMA_KNOWLEDGE = {
    "who": {
        "answer": "Amma is a spiritual leader and humanitarian who has dedicated her life to serving humanity. She grew up seeing poverty and suffering closely, and instead of turning away, she chose to help. From caring for elderly people in her village, her compassion grew into a global mission of education, healthcare, housing, and disaster relief. Today, Amma's vision is that compassion should not stop with the person standing in front of us—it can become education, healthcare, housing, disaster relief, environmental protection and opportunities for people to rebuild their lives.",
        "followup": "Would you like to know more about her service, compassion, or Amrita's mission?"
    },
    "amma": {
        "answer": "Amma is a spiritual leader and humanitarian who has dedicated her life to serving humanity. She grew up seeing poverty and suffering closely, and instead of turning away, she chose to help. From caring for elderly people in her village, her compassion grew into a global mission of education, healthcare, housing, and disaster relief. Today, Amma's vision is that compassion should not stop with the person standing in front of us—it can become education, healthcare, housing, disaster relief, environmental protection and opportunities for people to rebuild their lives.",
        "followup": "Would you like to know more about her service, compassion, or Amrita's mission?"
    },
    "service": {
        "answer": "If another person's suffering touches your heart, let your hands become part of the solution. Amma chose a life of service by caring for elderly and suffering people in her village without any grand plan—just genuine care. That small act became the beginning of a much larger journey that now reaches people across the world.",
        "followup": "Would you like to know how compassion becomes action?"
    },
    "compassion": {
        "answer": "Compassion becomes powerful when it moves from the heart to the hands. During the 2004 tsunami, Amma didn't just distribute relief—she walked into the water with children who were afraid and taught them to swim. Sometimes compassion doesn't need words. Sometimes it simply walks beside you into the water.",
        "followup": "That's the power of compassion. Want to know more?"
    },
    "love": {
        "answer": "For Amma, love is not just a word. Love becomes: food for someone who is hungry, healthcare for someone who is suffering, a home for someone who has lost everything, education for someone seeking opportunity, and comfort for someone who feels alone. Love is service. Service is action. Action is change.",
        "followup": "Love is action. Want to know more about how Amrita serves?"
    },
    "education": {
        "answer": "Education should give us knowledge, but also teach us how to use that knowledge responsibly—to solve problems, serve communities and improve lives. A degree shows what we know. Our actions show what we value. The highest purpose of knowledge is not simply to know more, but to do more good.",
        "followup": "True education connects knowledge with service. Interested in learning more?"
    },
    "amrita": {
        "answer": "Amrita Vishwa Vidyapeetham is Amma's institution that connects knowledge with real-world problems. Education develops people. Research develops solutions. Technology makes those solutions possible. Healthcare serves human needs. When knowledge leaves the classroom and reaches someone in need, education becomes service.",
        "followup": "Amrita's mission is beautiful. Want to know more?"
    },
    "technology": {
        "answer": "Technology can process information, detect problems, analyze data and build solutions. But it cannot replace genuine empathy, dignity, compassion and human connection. A machine asks 'What is the problem?' A compassionate human asks 'What is this person going through?' That difference matters.",
        "followup": "Technology is a tool, but compassion is what matters most. Want to know more?"
    },
    "environment": {
        "answer": "Protecting the environment is also an act of love. When we see waste in water, we should see the water it pollutes, the animals affected, the communities that depend on it, and future generations who will inherit what we leave. That is where Crafty Crab comes in—because protecting the environment is also an act of love.",
        "followup": "Environmental protection is service to future generations. Anything else you'd like to know?"
    },
    "tsunami": {
        "answer": "During the 2004 tsunami, Amma's response went beyond distributing relief. Children who became afraid of the sea were helped to face that fear. Amma even walked into the water with children and taught them to swim. Sometimes compassion does not need a speech. Sometimes it simply walks beside you into the water.",
        "followup": "That's true compassion in action. Want to know more?"
    }
}

def find_answer(question):
    question = question.lower()
    
    # Check for keyword matches
    for keyword, content in AMMA_KNOWLEDGE.items():
        if keyword in question:
            return content
    
    # Default response
    return {
        "answer": "Amma teaches us that Love is the Answer. I can tell you about: Amma herself, her service, compassion, love, education, Amrita, technology, environment, or the tsunami story. What interests you?",
        "followup": "What would you like to learn about?"
    }
