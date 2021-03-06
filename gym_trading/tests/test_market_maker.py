import unittest
from datetime import datetime as dt
import gym
from gym_trading.envs.market_maker import MarketMaker
import gym_trading


class MarketMakerTestCases(unittest.TestCase):

    def test_market_maker_gym_trade_completion(self):
        start_time = dt.now()

        config = {
            'training': False, 'fitting_file': 'BTC-USD_2019-04-07.csv.xz',
            'testing_file': 'BTC-USD_2019-04-08.csv.xz', 'step_size': 1,
            'max_position': 5, 'window_size': 20, 'seed': 1, 'action_repeats': 10,
            'format_3d': False, 'z_score': False, 'reward_type': 'trade_completion',
            'scale_rewards': False, 'ema_alpha': 0.99, 'transaction_fee': None,
        }
        print("**********\n{}\n**********".format(config))

        env = gym.make(MarketMaker.id, **config)
        total_reward = 0.0
        reward_list = []

        i = 0
        done = False
        env.reset()

        while not done:
            i += 1

            if i % 300 == 0:
                action = 10  # np.random.randint(env.action_space.n)  # break
            else:
                action = 0

            state, reward, done, _ = env.step(action)
            total_reward += reward
            reward_list.append(reward)

            if abs(reward) > 0.0001:
                print('reward = {:.4f} on step #{}'.format(reward, i))
            # env.render()

            if done:
                elapsed = (dt.now() - start_time).seconds
                print('Done on step #%i @ %i steps/second' % (
                    i, (i // elapsed) * env.action_repeats))
                print("Max reward: {}\nMin reward: {}".format(max(reward_list),
                                                              min(reward_list)))
                break

        env.reset()
        print('Total reward: %.4f' % total_reward)
        self.assertEqual(True, done)

    def test_market_maker_gym_continuous_reward(self):
        start_time = dt.now()

        config = {
            'training': False, 'fitting_file': 'BTC-USD_2019-04-07.csv.xz',
            'testing_file': 'BTC-USD_2019-04-08.csv.xz', 'step_size': 1,
            'max_position': 5, 'window_size': 20, 'seed': 1, 'action_repeats': 10,
            'format_3d': False, 'z_score': False, 'reward_type': 'continuous_total_pnl',
            'scale_rewards': False, 'ema_alpha': 0.99, 'transaction_fee': None,
        }
        print("**********\n{}\n**********".format(config))

        env = gym.make(MarketMaker.id, **config)
        total_reward = 0.0

        i = 0
        done = False
        env.reset()

        while not done:
            i += 1

            if i % 300 == 0:
                action = 10  # np.random.randint(env.action_space.n)  # break
            else:
                action = 0

            state, reward, done, _ = env.step(action)
            total_reward += reward

            if abs(reward) > 0.0001:
                print('reward = {:.4f} on step #{}'.format(
                    reward, env.env.local_step_number))
            # env.render()

            if done or i > 20000:
                elapsed = (dt.now() - start_time).seconds
                print('Done on step #%i @ %i steps/second' % (
                    i, (i // elapsed) * env.action_repeats))
                break

        env.reset()
        print('Total reward: %.4f' % total_reward)
        self.assertEqual(True, done)

    def test_market_maker_gym_asymmetrical_reward(self):
        start_time = dt.now()

        config = {
            'training': False, 'fitting_file': 'BTC-USD_2019-04-07.csv.xz',
            'testing_file': 'BTC-USD_2019-04-08.csv.xz', 'step_size': 1,
            'max_position': 5, 'window_size': 20, 'seed': 1, 'action_repeats': 10,
            'format_3d': False, 'z_score': False, 'reward_type': 'asymmetrical',
            'scale_rewards': False, 'ema_alpha': 0.99, 'transaction_fee': None,
        }
        print("**********\n{}\n**********".format(config))

        env = gym.make(MarketMaker.id, **config)
        total_reward = 0.0

        i = 0
        done = False
        env.reset()

        while not done:
            i += 1

            if i % 300 == 0:
                action = 10  # np.random.randint(env.action_space.n)  # break
            else:
                action = 0

            state, reward, done, _ = env.step(action)
            total_reward += reward

            if abs(reward) > 0.001:
                print('reward = {:.4f} on step #{}'.format(
                    reward, env.env.local_step_number))
            # env.render()

            if done or i > 20000:
                elapsed = (dt.now() - start_time).seconds
                print('Done on step #%i @ %i steps/second' % (
                    i, (i // elapsed) * env.action_repeats))
                break

        env.reset()
        print('Total reward: %.4f' % total_reward)
        self.assertEqual(True, done)

    def test_market_maker_action_space(self):
        start_time = dt.now()

        config = {
            'training': False, 'fitting_file': 'BTC-USD_2019-04-07.csv.xz',
            'testing_file': 'BTC-USD_2019-04-08.csv.xz', 'step_size': 1,
            'max_position': 5, 'window_size': 20, 'seed': 1, 'action_repeats': 10,
            'format_3d': False, 'z_score': False, 'reward_type': 'default',
            'scale_rewards': True, 'ema_alpha': [0.99, 0.999],
        }
        print("**********\n{}\n**********".format(config))

        env = gym.make(MarketMaker.id, **config)
        env.reset()

        def take_step(action: int, total_reward: float):
            # print("[TEST] take_step: action={}, total_reward={:.2f}".format(
            #     action, total_reward))
            state, reward, done, _ = env.step(action)
            total_reward += reward
            return state, reward, done, total_reward

        total_reward = 0.0
        action = 1  # skew long
        state, reward, done, total_reward = take_step(action, total_reward)

        action = 0
        for i in range(1000):
            state, reward, done, total_reward = take_step(action, total_reward)

        action = 4  # skew short
        state, reward, done, total_reward = take_step(action, total_reward)

        action = 0
        for i in range(1000):
            state, reward, done, total_reward = take_step(action, total_reward)

        self.assertEqual(False, env.env.broker.realized_pnl < 0.)

        action = 4  # skew short
        state, reward, done, total_reward = take_step(action, total_reward)
        action = 4  # skew short
        state, reward, done, total_reward = take_step(action, total_reward)
        action = 4  # skew short
        state, reward, done, total_reward = take_step(action, total_reward)

        action = 0
        for i in range(1000):
            state, reward, done, total_reward = take_step(action, total_reward)

        print(env.env.broker)
        self.assertEqual(3, env.env.broker.long_inventory.total_trade_count)
        self.assertEqual(3, env.env.broker.short_inventory.total_trade_count)

        elapsed = (dt.now() - start_time).seconds
        print("test_market_maker_action_space completed in {} seconds.".format(elapsed))


if __name__ == '__main__':
    unittest.main()
