import ReadingTime from '../src/components/vue/blog/ReadingTime.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof ReadingTime> = {
  title: 'Blog/ReadingTime',
  component: ReadingTime,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Reading time indicator component that calculates estimated reading time based on text content.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

const shortText = 'This is a short article with minimal content. Just a few sentences to demonstrate the reading time calculation.'

const mediumText = `This is a medium-length article that contains multiple paragraphs and provides more detailed information about a topic.
  
  The article covers various aspects of the subject matter and includes examples and explanations that help readers understand the concepts better.
  
  With several hundred words, this article would typically take a few minutes to read completely, making it a good example for testing the reading time calculation.`

const longText = `This is a comprehensive, long-form article that dives deep into a complex topic with extensive detail and analysis.
  
  The article begins with an introduction that sets the context and explains why the topic matters. It then proceeds to explore various subtopics, each with its own section and detailed explanations.
  
  Throughout the article, readers will find numerous examples, code snippets, and practical applications that illustrate the concepts being discussed. The writing is thorough and takes time to explain nuances and edge cases.
  
  The article also includes comparisons with alternative approaches, discusses best practices, and provides recommendations based on real-world experience and research.
  
  By the time readers finish this article, they will have gained a comprehensive understanding of the topic and will be well-equipped to apply the knowledge in their own work.
  
  The conclusion summarizes the key points and provides additional resources for those who want to learn more about the subject.`.repeat(3)

export const ShortArticle: Story = {
  render: (args) => ({
    components: { ReadingTime },
    setup() {
      return { args }
    },
    template: '<ReadingTime v-bind="args" />'
  }),
  args: {
    text: shortText
  }
}

export const MediumArticle: Story = {
  render: (args) => ({
    components: { ReadingTime },
    setup() {
      return { args }
    },
    template: '<ReadingTime v-bind="args" />'
  }),
  args: {
    text: mediumText
  }
}

export const LongArticle: Story = {
  render: (args) => ({
    components: { ReadingTime },
    setup() {
      return { args }
    },
    template: '<ReadingTime v-bind="args" />'
  }),
  args: {
    text: longText
  }
}

export const CustomReadingSpeed: Story = {
  render: (args) => ({
    components: { ReadingTime },
    setup() {
      return { args }
    },
    template: '<ReadingTime v-bind="args" />'
  }),
  args: {
    text: mediumText,
    wordsPerMinute: 150
  }
}
